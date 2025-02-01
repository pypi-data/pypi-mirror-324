import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.routing import APIRoute
from pickle_util import save_data, get_all_data
import uuid

logger = logging.getLogger(__name__)


class DynamicApi:
    def __init__(self, app: FastAPI, log) -> None:
        self.bot = None
        self.app = app
        self.log = log
        self.hooks = {}

    def set_bot(self, bot):
        self.bot = bot

    def add_dynamic_endpoint(self, hook_id: str):
        async def dynamic_handler(request: Request, route_path: str):
            data = await request.json()
            self.log.info(data)
            if self.bot:
                await self.bot.forward_webhook_message(route_path, data)
            return {
                "message": f"Received data for webhook {hook_id} @ {route_path}",
                "data": data,
            }

        hook_uuid = uuid.uuid4()
        route_path = f"/webhook-bot/{hook_uuid}"
        self.app.add_api_route(route_path, dynamic_handler, methods=["POST"])

        self.hooks.update({hook_id: route_path})
        save_data({"hooks": self.hooks})
        return route_path

    def remove_dynamic_endpoint(self, hook_id: str):
        route_path = self.hooks.get(hook_id)
        if not route_path:
            raise HTTPException(status_code=404, detail=f"Webhook {hook_id} not found")

        self.app.router.routes = [
            route
            for route in self.app.router.routes
            if not (isinstance(route, APIRoute) and route.path == route_path)
        ]

        self.hooks.pop(hook_id)
        save_data({"hooks": self.hooks})

    def load_persisted_endpoints(self):
        hooks = get_all_data().get("hooks")
        if hooks is not None:
            for hook_key in hooks.keys():
                self.add_dynamic_endpoint(hook_key)
        logger.info(f"Loaded the following hooks:\n{self.hooks}")
        return self.hooks

    def list_endpoints(self):
        return self.hooks
