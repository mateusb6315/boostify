from discord.ext import commands
import discord
import os
import asyncio
from config.vars import TOKEN

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("bb."), intents=discord.Intents.all()
)


async def carregar_cogs():
    for arquivo in os.listdir("./cogs"):
        if arquivo.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{arquivo[:-3]}")
                print(f"Log: Cog {arquivo} carregada com sucesso.")
            except Exception as erro:
                print(f"Log: Erro ao carregar {arquivo}: {erro}")


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Log: Comandos sincronizados")
    print(f"Log: Bot online como {bot.user}")


async def main():
    async with bot:
        await carregar_cogs()
        print("Log: Cogs carregados")
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
