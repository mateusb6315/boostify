from discord.ext import commands
import discord
from config.vars import DOUBLEBOOSTER_ID, CANAL_ID


class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    def _get_gestordados_cog(self):
        cog = self.bot.get_cog("GestorDados")
        if cog is None:
            print("Erro: Cog GestorDados não carregada")
        return cog

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        servidor = after.guild
        onebooster = servidor.premium_subscriber_role
        doublebooster = servidor.get_role(DOUBLEBOOSTER_ID)

        if onebooster in before.roles and onebooster not in after.roles:
            if doublebooster and doublebooster in after.roles:
                await after.remove_roles(doublebooster)

            canal = after.guild.get_channel(CANAL_ID)
            if canal:
                await canal.send(f"❌ {after.mention} não é mais Booster")

            gestor = self._get_gestordados_cog()
            if gestor:
                await gestor.atualizarBoost(after, 0)

    @commands.Cog.listener()
    async def on_message(self, mensagem):
        if mensagem.guild is None:
            return

        if mensagem.channel.id != CANAL_ID:
            return

        if mensagem.type not in [
            discord.MessageType.premium_guild_subscription,
            discord.MessageType.premium_guild_tier_1,
            discord.MessageType.premium_guild_tier_2,
            discord.MessageType.premium_guild_tier_3,
        ]:
            return

        usuariobooster = mensagem.author

        gestor = self._get_gestordados_cog()
        if gestor is None:
            return

        qtd_boosts = await gestor.adicionarBoost(usuariobooster)
        if qtd_boosts >= 2:
            doublebooster = mensagem.guild.get_role(DOUBLEBOOSTER_ID)
            if doublebooster:
                await mensagem.author.add_roles(doublebooster)
                await mensagem.channel.send(
                    f"{mensagem.author.mention} virou Super Booster 🚀"
                )
            else:
                print("Erro: Cargo doublebooster não encontrado")
        else:
            await mensagem.channel.send(f"🎉 {mensagem.author.mention} virou Booster!")


async def setup(bot):
    await bot.add_cog(Eventos(bot))
