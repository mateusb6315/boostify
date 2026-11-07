import logging

import discord
from discord.ext import commands

log = logging.getLogger(__name__)
BOOST_TYPES = {discord.MessageType.premium_guild_subscription,
               discord.MessageType.premium_guild_tier_1,
               discord.MessageType.premium_guild_tier_2,
               discord.MessageType.premium_guild_tier_3}


async def sync_role(member, role, count):
    if role is None:
        raise ValueError("Cargo double booster não encontrado")
    if count >= 2 and role not in member.roles:
        await member.add_roles(role, reason="Contagem de boosts")
    elif count < 2 and role in member.roles:
        await member.remove_roles(role, reason="Contagem de boosts")


class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def process_boost(self, message):
        store = self.bot.get_cog("GestorDados")
        config = store.read("config")
        if (message.guild is None or message.guild.id != config.get("guild_id")
                or message.channel.id != config.get("channel_id")
                or message.type not in BOOST_TYPES):
            return False
        count = await store.record_message(message.id, message.author.id)
        if count is None:
            return False
        member = message.guild.get_member(message.author.id)
        role = message.guild.get_role(config.get("role_id"))
        if member and role:
            try:
                await sync_role(member, role, count)
            except discord.HTTPException:
                log.exception("Falha ao sincronizar cargo para usuário %s", message.author.id)
        else:
            log.warning("Membro ou cargo indisponível para mensagem %s", message.id)
        return True

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.process_boost(message)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        store = self.bot.get_cog("GestorDados")
        config = store.read("config")
        if after.guild.id != config.get("guild_id"):
            return
        booster = after.guild.premium_subscriber_role
        if booster and booster in before.roles and booster not in after.roles:
            await store.set_count(after.id, 0)
            role = after.guild.get_role(config.get("role_id"))
            if role:
                try:
                    await sync_role(after, role, 0)
                except discord.HTTPException:
                    log.exception("Falha ao remover cargo de %s", after.id)


async def setup(bot):
    await bot.add_cog(Eventos(bot))
