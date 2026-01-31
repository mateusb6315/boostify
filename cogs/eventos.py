from discord.ext import commands
import discord


DOUBLEBOOSTER_ID = 1294435658210869259
CANAL_ID = 1294435658797944842


class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    def _get_boosts_cog(self):
        cog = self.bot.get_cog("Boosts")
        if cog is None:
            print("Erro: Cog Boosts não carregada")
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
                await canal.send(f"{after.mention} não é mais Booster")

            boosts_cog = self._get_boosts_cog()
            if boosts_cog:
                await boosts_cog.atualizarBoostDB(after, 0)

    @commands.Cog.listener()
    async def on_message(self, mensagem):
        if mensagem.guild is None:
            return

        if mensagem.guild.get_channel(CANAL_ID) is None:
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

        boosts_cog = self._get_boosts_cog()
        if boosts_cog is None:
            return

        qtd_boosts = await boosts_cog.adicionarBoostDB(usuariobooster)

        if qtd_boosts >= 2:
            doublebooster = mensagem.guild.get_role(DOUBLEBOOSTER_ID)
            if doublebooster:
                await mensagem.author.add_roles(doublebooster)
                await mensagem.channel.send(
                    f"{mensagem.author.mention} virou 2x booster"
                )
            else:
                print("Erro: Cargo doublebooster não encontrado")
        else:
            await mensagem.channel.send(f"{mensagem.author.mention} virou 1x booster")


async def setup(bot):
    await bot.add_cog(Eventos(bot))
