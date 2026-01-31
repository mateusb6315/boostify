import os
import json
from discord.ext import commands
from config.vars import DIRETORIO_BOOSTS


class GestorDados(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self._garantir_arquivo()

    def _garantir_arquivo(self):
        os.makedirs(os.path.dirname(DIRETORIO_BOOSTS), exist_ok=True)
        if not os.path.exists(DIRETORIO_BOOSTS):
            with open(DIRETORIO_BOOSTS, "w") as arquivo:
                json.dump({}, arquivo)

    def ler_json(self):
        with open(DIRETORIO_BOOSTS, "r") as arquivo:
            return json.load(arquivo)

    def gravar_json(self, data):
        with open(DIRETORIO_BOOSTS, "w") as arquivo:
            json.dump(data, arquivo, indent=4)

    async def atualizarBoost(self, usuario, boosts):
        dados = self.ler_json()
        usuario_id_str = str(usuario.id)
        dados[usuario_id_str] = {"boosts": boosts}
        self.gravar_json(dados)
        return dados[usuario_id_str]

    async def adicionarBoost(self, usuario):
        usuario_id_str = str(usuario.id)
        dados = self.ler_json()
        if usuario_id_str not in dados:
            dados[usuario_id_str] = {"boosts": 1}
        else:
            dados[usuario_id_str]["boosts"] += 1
        self.gravar_json(dados)
        return dados[usuario_id_str]["boosts"]

    async def obterBoosts(self, usuario):
        usuario_id_str = str(usuario.id)
        dados = self.ler_json()
        return dados.get(usuario_id_str, {"boosts": 0})["boosts"]


async def setup(bot):
    await bot.add_cog(GestorDados(bot))
