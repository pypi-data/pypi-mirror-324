from mautrix.client import Client
from mautrix.types import (
    EventType,
    Filter,
    Format,
    RoomFilter,
    UserID,
    RoomID,
    PowerLevelStateEventContent,
    TextMessageEventContent,
    MessageType,
)
from mautrix.client.state_store import FileStateStore
from typing import Optional
from api import DynamicApi
from fastapi import HTTPException
from jinja2 import Template
from emoji import emojize
from pickle_util import save_data, get_data

import os
import configparser


class WebhookBot:
    def __init__(self, api: "DynamicApi", log, listen_port):
        self._client: Optional[Client] = None
        self.event_id = None
        self.latest_timestamp = 32503723200000
        self.bot_controll_room_id = RoomID("")
        self.bot_output_room_id = RoomID("")
        self.api = api
        self.api.set_bot(self)
        self.log = log
        self.homeserver_url = ""
        self.token = ""
        self.admin_user = UserID("")
        self.bot_user = UserID("")
        self.listen_port = listen_port
        self.device_id = "AAAAAAAAAA"

    @property
    def client(self) -> Client:
        if not self._client:
            raise RuntimeError("Client not initialized")
        return self._client

    async def load_config(self, file_path="config/config.ini"):
        config = configparser.ConfigParser()
        config.read(file_path)
        self.homeserver_url = os.getenv(
            "HOMESERVER_URL", config.get("settings", "homeserver_url", fallback=None)
        )
        admin_user = os.getenv(
            "ADMIN_USER", config.get("settings", "admin_user", fallback=None)
        )
        bot_user = os.getenv(
            "BOT_USER", config.get("settings", "bot_user", fallback=None)
        )
        self.token = os.getenv("TOKEN", config.get("settings", "token", fallback=None))
        self.device_id = os.getenv(
            "DEVICE_ID", config.get("settings", "device_id", fallback=None)
        )
        if not (
            self.homeserver_url
            and admin_user
            and bot_user
            and self.token
            and self.device_id
        ):
            raise ValueError(f"""Configuration is missing, recheck 
            homeserver_url: {self.homeserver_url}\n
            admin_user: {admin_user}\n
            bot_user: {bot_user}\n
            token: {self.token}""")
        self.admin_user = UserID(admin_user)
        self.bot_user = UserID(bot_user)

    async def start(self):
        await self.load_config()
        self.log.info(self.bot_user)
        loaded_hooks = self.api.load_persisted_endpoints()
        store_path = "./state_store"
        state_store = FileStateStore(store_path)
        self._client = Client(
            mxid=self.bot_user,
            device_id=self.device_id,
            state_store=state_store,
            base_url=self.homeserver_url,
            token=self.token,
        )
        await self.setup_controll_room()
        await self.setup_output_room()

        self.event_id = await self.client.send_notice(
            self.bot_controll_room_id, "Matrix webhook bot started!"
        )
        if loaded_hooks != {} and loaded_hooks is not None:
            template_text = self.load_template("webhooks_message")
            if template_text is None:
                self.event_id = await self.client.send_notice(
                    self.bot_controll_room_id,
                    f"""Persisted webhooks are available, but the webhooks_message.jinja is missing from the templated folder.
                 Webhooks in json format {loaded_hooks}""",
                )
            else:
                rendered_message = Template(template_text).render(webhooks=loaded_hooks)
                self.event_id = await self.client.send_notice(
                    self.bot_controll_room_id, rendered_message
                )
        self.client.add_event_handler(EventType.ROOM_MESSAGE, self.process_message)
        self.client.start(Filter(room=RoomFilter(rooms=[self.bot_controll_room_id])))

    async def stop(self):
        self.client.stop()

    async def handle_list(self, event):
        endpoints = self.api.list_endpoints()
        await self.send_response(event, f"Here is the list of webhooks.\n{endpoints}")

    async def handle_help(self, event):
        help_message = (
            "Available commands:\n"
            "!webhook list - List all webhooks\n"
            "!webhook help - Show this help message\n"
            "!webhook add rss - Add an RSS webhook\n"
            "!webhook remove rss - Remove an RSS webhook"
        )
        await self.send_response(event, help_message)

    async def handle_add(self, event, argument):
        route_path = self.api.add_dynamic_endpoint(argument)
        await self.send_response(
            event,
            f"""{argument} webhook added.
Use the following url: {self.homeserver_url}{route_path}
Don't forget to add this to your reverse proxy config
I'm running on port {self.listen_port}""",
        )

    async def handle_remove(self, event, argument):
        try:
            self.api.remove_dynamic_endpoint(argument)
        except HTTPException:
            await self.send_response(
                event, f"{argument} webhook is not available, didn't remove."
            )
        await self.send_response(event, f"{argument} webhook removed.")

    async def process_message(self, event):
        if event.event_id == self.event_id:
            self.latest_timestamp = event.timestamp
        if event.timestamp > self.latest_timestamp and self.event_id is not None:
            content = event.content.body.strip()
            if content.startswith("!webhook"):
                parts = content.split(maxsplit=2)
                command = parts[1] if len(parts) > 1 else None
                argument = parts[2] if len(parts) > 2 else None

                if command == "list":
                    await self.handle_list(event)
                elif command == "help":
                    await self.handle_help(event)
                elif command == "add" and argument:
                    await self.handle_add(event, argument)
                elif command == "remove" and argument:
                    await self.handle_remove(event, argument)
                else:
                    await self.send_response(
                        event, "Invalid command or missing argument."
                    )

    async def send_response(self, event, message: str):
        await self.client.send_notice(event.room_id, message)

    async def forward_webhook_message(self, hook_id, route_path: str, msg: str):
        flattened_data = self.flatten_dict(msg)
        self.log.info(flattened_data)
        template_text = self.load_template(hook_id)
        if template_text is None:
            await self.client.send_notice(
                self.bot_output_room_id,
                f"Service sent us a message to {self.homeserver_url}/{route_path}, but there is no template for it\r\n"
                f"this is the message\r\n{msg}",
            )

        else:
            rendered_message = Template(template_text).render(flattened_data)
            emojized_message = emojize(rendered_message)
            await self.client.send_message(
                self.bot_output_room_id,
                content=TextMessageEventContent(
                    format=Format.HTML,
                    formatted_body=emojized_message.replace("\n", "<br>"),
                    msgtype=MessageType.TEXT,
                ),
            )

    def flatten_dict(self, nested_dict, parent_key="", separator="_"):
        flattened_items = []
        for key, value in nested_dict.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key
            if isinstance(value, dict):
                flattened_items.extend(
                    self.flatten_dict(value, new_key, separator=separator).items()
                )
            else:
                flattened_items.append((new_key, value))
        return dict(flattened_items)

    def load_template(self, hook_id: str):
        file_path = f"config/templates/{hook_id}.jinja"
        try:
            with open(file_path, "r", encoding="utf-8") as template:
                return template.read()
        except FileNotFoundError:
            self.log.error(f"Error: File not found - {file_path}")
            return None
        except Exception as e:
            self.log.error(f"Error: {str(e)}")
            return None

    async def setup_controll_room(self):
        controll_room_welcome_message = "Hello from matrix webhook bot!\nThis is the controll room, feel free to ask !webhook help"

        self.bot_controll_room_id = get_data("bot_controll_room_id")

        if self.bot_controll_room_id == "":
            self.bot_controll_room_id = await self.client.create_room(
                name="Webhook bot controll room",
                topic="Controll Webhook bot",
                is_direct=True,
                invitees=[self.admin_user],
            )
            save_data({"bot_controll_room_id": self.bot_controll_room_id})
            powerLevelStateEventContent = PowerLevelStateEventContent(
                users={self.admin_user: 100, self.bot_user: 100}
            )
            await self.client.send_state_event(
                room_id=self.bot_controll_room_id,
                event_type=EventType("m.room.power_levels", EventType.Class.STATE),
                content=powerLevelStateEventContent,
            )
            await self.client.send_notice(
                self.bot_controll_room_id, controll_room_welcome_message
            )

    async def setup_output_room(self):
        self.bot_output_room_id = get_data("bot_output_room_id")
        if self.bot_output_room_id == "":
            self.bot_output_room_id = await self.client.create_room(
                name="Webhook bot",
                topic="Webhook bot output room",
                is_direct=True,
                invitees=[self.admin_user],
            )
            save_data({"bot_output_room_id": self.bot_output_room_id})
            await self.client.send_notice(
                self.bot_output_room_id,
                "Hello from matrix webhook bot! This is the output room for incoming webhook messages.",
            )
