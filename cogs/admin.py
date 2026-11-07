import discord
from discord.ext import commands

from cogs.eventos import sync_role


def authorized():
    async def predicate(ctx):
        if ctx.guild is None:
            return False
        store = ctx.bot.get_cog("GestorDados")
        config = store.read("config")
        if config.get("guild_id") not in (None, ctx.guild.id):
            return False
        if await ctx.bot.is_owner(ctx.author) or ctx.author.guild_permissions.administrator:
            return True
        trusted = store.read("admins")["role_ids"]
        return any(role.id in trusted for role in ctx.author.roles)
    return commands.check(predicate)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def store(self):
        return self.bot.get_cog("GestorDados")

    @commands.group(name="config", invoke_without_command=True)
    @authorized()
    async def config(self, ctx):
        """Configure o canal e o cargo existentes neste servidor."""
        data = self.store.read("config")
        await ctx.send(f"Canal: <#{data['channel_id']}>" if data.get("channel_id") else "Canal não configurado.")
        await ctx.send(f"Cargo: <@&{data['role_id']}>" if data.get("role_id") else "Cargo não configurado.")

    @config.command(name="canal")
    @authorized()
    async def channel(self, ctx, channel: discord.TextChannel):
        data = self.store.read("config")
        data.update(guild_id=ctx.guild.id, channel_id=channel.id)
        self.store.write("config", data)
        await ctx.send(f"Canal de rastreamento definido: {channel.mention}.")

    @config.command(name="cargo")
    @authorized()
    async def role(self, ctx, role: discord.Role):
        data = self.store.read("config")
        data.update(guild_id=ctx.guild.id, role_id=role.id)
        self.store.write("config", data)
        await ctx.send(f"Cargo double booster definido: {role.mention}.")

    @commands.group(name="confiavel", invoke_without_command=True)
    @authorized()
    async def trusted(self, ctx):
        roles = self.store.read("admins")["role_ids"]
        await ctx.send("Cargos confiáveis: " + (", ".join(f"<@&{r}>" for r in roles) if roles else "nenhum"))

    @trusted.command(name="add")
    @authorized()
    async def trusted_add(self, ctx, role: discord.Role):
        # Delegação de privilégios é reservada ao dono e a administradores.
        if not (await self.bot.is_owner(ctx.author) or ctx.author.guild_permissions.administrator):
            return await ctx.send("Somente o dono do bot ou administradores podem alterar cargos confiáveis.")
        data = self.store.read("admins")
        if role.id not in data["role_ids"]:
            data["role_ids"].append(role.id)
            self.store.write("admins", data)
        await ctx.send("Cargo confiável adicionado.")

    @trusted.command(name="rm")
    @authorized()
    async def trusted_remove(self, ctx, role: discord.Role):
        if not (await self.bot.is_owner(ctx.author) or ctx.author.guild_permissions.administrator):
            return await ctx.send("Somente o dono do bot ou administradores podem alterar cargos confiáveis.")
        data = self.store.read("admins")
        if role.id in data["role_ids"]:
            data["role_ids"].remove(role.id)
            self.store.write("admins", data)
        await ctx.send("Cargo confiável removido.")

    @commands.command(name="view")
    @authorized()
    async def view(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f"{member.mention}: {self.store.count(member.id)} boost(s) registrado(s).")

    @commands.command(name="setboost")
    @authorized()
    async def setboost(self, ctx, member: discord.Member, count: int):
        if count < 0:
            return await ctx.send("A contagem não pode ser negativa.")
        config = self.store.read("config")
        role = ctx.guild.get_role(config.get("role_id"))
        if role is None:
            return await ctx.send("Configure primeiro o cargo double booster.")
        await self.store.set_count(member.id, count)
        try:
            await sync_role(member, role, count)
        except discord.HTTPException:
            return await ctx.send("Contagem salva, mas não foi possível atualizar o cargo. Verifique permissões e hierarquia.")
        await ctx.send(f"Contagem de {member.mention} definida como {count}.")

    @commands.command(name="sincronizar")
    @authorized()
    async def sync_history(self, ctx):
        """Processa mensagens disponíveis no histórico sem contá-las duas vezes."""
        config = self.store.read("config")
        channel = ctx.guild.get_channel(config.get("channel_id"))
        if channel is None or ctx.guild.get_role(config.get("role_id")) is None:
            return await ctx.send("Configure primeiro o canal e o cargo.")
        await ctx.send("Lendo histórico disponível; isso pode demorar.")
        count = 0
        try:
            async for message in channel.history(limit=None, oldest_first=True):
                if await self.bot.get_cog("Eventos").process_boost(message):
                    count += 1
        except discord.HTTPException:
            return await ctx.send("Não foi possível ler todo o histórico. Verifique as permissões e tente novamente.")
        await ctx.send(f"Sincronização concluída: {count} mensagem(ns) nova(s) processada(s).")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Você não tem permissão para usar este comando neste servidor.")
        elif isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument)):
            await ctx.send(f"Argumentos inválidos. Consulte `{ctx.prefix}help {ctx.command}`.")


async def setup(bot):
    await bot.add_cog(Admin(bot))
