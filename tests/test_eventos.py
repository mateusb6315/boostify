import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import discord
from cogs.eventos import Eventos
from cogs.gestor import GestorDados


def test_only_configured_channel_is_processed_once(tmp_path):
    async def run():
        store = GestorDados(None, tmp_path)
        store.write("config", {"guild_id": 1, "channel_id": 2, "role_id": 3})
        role = object()
        member = SimpleNamespace(id=4, roles=[], add_roles=AsyncMock(), remove_roles=AsyncMock())
        guild = SimpleNamespace(id=1, get_member=lambda _: member, get_role=lambda _: role)
        message = SimpleNamespace(id=5, guild=guild, channel=SimpleNamespace(id=2),
                                  type=discord.MessageType.premium_guild_subscription, author=member)
        bot = SimpleNamespace(get_cog=lambda _: store)
        cog = Eventos(bot)
        assert await cog.process_boost(message)
        assert not await cog.process_boost(message)
        message.channel.id = 9
        message.id = 6
        assert not await cog.process_boost(message)
        assert store.count(4) == 1
    asyncio.run(run())
