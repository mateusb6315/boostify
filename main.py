from discord.ext import commands
import discord
import os
import asyncio
from dotenv import load_dotenv

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("cob."), intents=discord.Intents.all()
)


async def carregar_cogs():
    for arquivo in os.listdir("./cogs"):
        if arquivo.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{arquivo[:-3]}")
                print(f"Cog {arquivo} carregada com sucesso.")
            except Exception as erro:
                print(f"Erro ao carregar {arquivo}: {erro}")


@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")


async def main():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    async with bot:
        await carregar_cogs()
        print("Cogs carregados")
        await bot.tree.sync()
        print("Comandos sincronizados")
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
