from discord.ext import commands
import typing


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cargo")
    async def cargo(
        self,
        ctx,
        nome_cargo: typing.Optional[str] = None,
        cor_cargo: typing.Optional[str] = None,
    ):
        if nome_cargo is None or cor_cargo is None:
            await ctx.send(
                "Uso correto: `bb.cargo <nome_cargo> <cor_cargo>`\nExemplo: `bb.cargo Fã de F1 #FF0000`"
            )
            return
        else:
            await ctx.send(f"Cargo: {nome_cargo}\nCor: {cor_cargo}")
            await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Utils(bot))
