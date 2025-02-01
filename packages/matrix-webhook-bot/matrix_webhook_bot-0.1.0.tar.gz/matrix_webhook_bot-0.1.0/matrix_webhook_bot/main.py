from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
import uvicorn
from webhook_bot import WebhookBot
from api import DynamicApi
from logger import BotLogger

listen_port = 8228
log = BotLogger()
bot = None  # Store bot instance globally


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown lifecycle"""
    global bot

    api = DynamicApi(app, log)
    bot = WebhookBot(api, log, listen_port)

    try:
        await bot.start()  # Start bot
        yield  # Hand over control to FastAPI
    finally:
        log.info("Shutting down bot...")
        if bot:
            try:
                await bot.stop()
                log.info("Bot stopped.")
            except asyncio.CancelledError:
                log.info("Bot shutdown was interrupted.")

        log.info("Lifespan shutdown complete.")


app = FastAPI(lifespan=lifespan)

async def run_uvicorn():
    """Run Uvicorn properly and handle shutdown"""
    config = uvicorn.Config(app, host="0.0.0.0", port=listen_port)
    server = uvicorn.Server(config)

    try:
        await server.serve()
    except asyncio.CancelledError:
        log.info("Uvicorn shutdown interrupted. Cleaning up...")


async def main():
    """Start Uvicorn and bot together"""
    await run_uvicorn()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Received KeyboardInterrupt, shutting down...")
