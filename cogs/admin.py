from discord.ext import commands
import discord
import asyncio
from config.vars import DOUBLEBOOSTER_ID, CANAL_ID


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def obter_gestordados_cog(self):
        cog = self.bot.get_cog("GestorDados")
        if cog is None:
            print("Erro: Cog GestorDados não carregada")
        return cog

    @commands.command(name="add")
    @commands.is_owner()
    async def adicionar_boost(self, ctx, usuario: discord.Member = None):
        """Adiciona um boost"""
        usuario = usuario or ctx.author
        gestor = self.obter_gestordados_cog()
        if not gestor:
            return await ctx.send("Erro: Cog GestorDados não encontrada")

        qtd_boosts = await gestor.adicionarBoost(usuario)
        await ctx.send(
            f"✅ Boost adicionado! {usuario.mention} agora tem {qtd_boosts} boost(s)"
        )

        if qtd_boosts >= 2:
            cargo = ctx.guild.get_role(DOUBLEBOOSTER_ID)
            if cargo:
                await usuario.add_roles(cargo)
                await ctx.send(f"🚀 {usuario.mention} recebeu o cargo Super Booster!")

    @commands.command(name="rm")
    @commands.is_owner()
    async def remover_boost(self, ctx, usuario: discord.Member = None):
        """Remove um boost de um usuário"""
        usuario = usuario or ctx.author
        gestor = self.obter_gestordados_cog()
        if not gestor:
            return await ctx.send("Erro: Cog GestorDados não encontrada")
        if await gestor.obterBoosts(usuario) == 0:
            return await ctx.send(
                f"❌ {usuario.mention} não tem boosts nesse servidor."
            )
        qtd_boosts = await gestor.removerBoost(usuario)
        await ctx.send(
            f"✅ Boost removido! {usuario.mention} agora tem {qtd_boosts} boost(s)"
        )

        if qtd_boosts < 2:
            cargo = ctx.guild.get_role(DOUBLEBOOSTER_ID)
            if cargo and cargo in usuario.roles:
                await usuario.remove_roles(cargo)
                await ctx.send(f"❌ {usuario.mention} perdeu o cargo Super Booster!")

    @commands.command(name="reset")
    @commands.is_owner()
    async def resetar_boost(self, ctx, usuario: discord.Member = None):
        """Reseta os boosts de um usuário"""
        usuario = usuario or ctx.author
        gestor = self.obter_gestordados_cog()
        if not gestor:
            return await ctx.send("Erro: Cog GestorDados não encontrada")
        if await gestor.obterBoosts(usuario) == 0:
            return await ctx.send(f"{usuario.mention} não tem boosts nesse servidor.")

        await gestor.atualizarBoost(usuario, 0)
        cargo = ctx.guild.get_role(DOUBLEBOOSTER_ID)
        if cargo and cargo in usuario.roles:
            await usuario.remove_roles(cargo)

        await ctx.send(f"↩️ Boosts de {usuario.mention} resetados!")

    @commands.command(name="view")
    @commands.is_owner()
    async def ver_boost(self, ctx, usuario: discord.Member = None):
        """Mostra quantos boosts um usuário tem"""
        usuario = usuario or ctx.author
        gestor = self.obter_gestordados_cog()
        if not gestor:
            return await ctx.send("Erro: Cog GestorDados não encontrada")

        qtd_boosts = await gestor.obterBoosts(usuario)
        await ctx.send(f"✏️ {usuario.mention} tem {qtd_boosts} boost(s)")

    @commands.command(name="list")
    @commands.is_owner()
    async def checar_boosts(self, ctx):
        """Checa todos os boosts registrados"""
        gestor = self.obter_gestordados_cog()
        if not gestor:
            return await ctx.send("Erro: Cog GestorDados não encontrada")
        dados = gestor.ler_json()
        mensagem = "📊 Boosts registrados:\n\n"
        if not dados:
            mensagem += "❌ Nenhum boost registrado."
        for usuario_id, info in dados.items():
            mensagem += (
                f"<@{usuario_id}>: {info['boosts']} boost(s)\n"
                if info["boosts"] > 0
                else ""
            )
        await ctx.send(mensagem)

    @commands.command(name="stats")
    @commands.is_owner()
    async def estatisticas(self, ctx):
        gestor = self.obter_gestordados_cog()
        dados = gestor.ler_json()

        total_boosters = sum(1 for info in dados.values() if info["boosts"] > 0)
        total_boosts = sum(info["boosts"] for info in dados.values())
        super_boosters = sum(1 for info in dados.values() if info["boosts"] >= 2)

        embed = discord.Embed(
            title="📊 Estatísticas de Boosts", color=discord.Color.magenta()
        )
        embed.add_field(
            name="Total de Boosters", value=str(total_boosters), inline=False
        )
        embed.add_field(name="Total de Boosts", value=str(total_boosts), inline=False)
        embed.add_field(
            name="Super Boosters (2+ boosts)", value=str(super_boosters), inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name="testecanal")
    @commands.is_owner()
    async def test_channel(self, ctx, canal: discord.TextChannel = None):
        """Testa o canal de notificações de boosts"""
        if canal is None:
            canal = ctx.guild.get_channel(CANAL_ID)
            if canal is None:
                await ctx.send(
                    "❌ O canal de notificações não existe ou não foi encontrado."
                )
            if canal.id == CANAL_ID:
                await ctx.send(
                    "✅ O canal de notificações está configurado corretamente."
                )

    @commands.command(name="testecargo")
    @commands.is_owner()
    async def test_role(self, ctx, cargo: discord.Role = None):
        if cargo is None:
            cargo = ctx.guild.get_role(DOUBLEBOOSTER_ID)
            if cargo is None:
                await ctx.send(
                    "❌ O cargo Super Booster não existe ou não foi encontrado."
                )
            if cargo.id == DOUBLEBOOSTER_ID:
                await ctx.send(
                    "✅ O cargo Super Booster está configurado corretamente."
                )

    @commands.command(name="limparjson")
    @commands.is_owner()
    async def limpar_json(self, ctx):
        """Limpa o arquivo JSON de boosts"""
        await ctx.send(
            "⚠️ Atenção: Isso irá apagar todos os dados de boosts.\n"
            'Tem certeza? Responda "sim" em até 10 segundos.'
        )

        def check(mensagem):
            return (
                mensagem.author == ctx.author
                and mensagem.channel == ctx.channel
                and mensagem.content.lower() == "sim"
            )

        try:
            await self.bot.wait_for("message", check=check, timeout=10)
        except asyncio.TimeoutError:
            return await ctx.send("⏱️ Tempo esgotado. Comando cancelado.")

        gestor = self.obter_gestordados_cog()
        if not gestor:
            return await ctx.send("Erro: Cog GestorDados não encontrada")
        await gestor.limpar_json()
        await ctx.send("✅ Arquivo JSON de boosts limpo!")


async def setup(bot):
    await bot.add_cog(Admin(bot))
