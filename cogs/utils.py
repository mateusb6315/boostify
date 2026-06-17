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
            await ctx.send(
                f"**Pedido de cargo**\n\n**Usuário**: {ctx.author.mention}\n**Cargo**: {nome_cargo}\n**Cor**: {cor_cargo}"
            )
            await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Utils(bot))
