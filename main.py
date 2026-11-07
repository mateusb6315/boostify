import asyncio
import logging

import discord
from discord.ext import commands

from config.vars import load_config

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class BoostBot(commands.Bot):
    async def setup_hook(self):
        for extension in ("cogs.gestor", "cogs.admin", "cogs.eventos"):
            await self.load_extension(extension)


async def main():
    config = load_config()
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = BoostBot(command_prefix=commands.when_mentioned_or(config.prefix), intents=intents)
    async with bot:
        await bot.start(config.token)


if __name__ == "__main__":
    asyncio.run(main())
