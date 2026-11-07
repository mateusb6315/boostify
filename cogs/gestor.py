import asyncio
import json
import os
import tempfile
from pathlib import Path

from discord.ext import commands
from config.vars import DATA_DIR


class GestorDados(commands.Cog):
    """Persistência local; cada instância pertence a um único servidor."""

    def __init__(self, bot, data_dir=None):
        self.bot = bot
        self.data_dir = Path(data_dir) if data_dir is not None else DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.lock = asyncio.Lock()
        for name, default in (("boosts", {"users": {}, "processed_messages": []}),
                              ("admins", {"role_ids": []}), ("config", {})):
            path = self.data_dir / f"{name}.json"
            if not path.exists():
                self.write(name, default)
        boosts = self.read("boosts")
        if not isinstance(boosts, dict) or not isinstance(boosts.get("users"), dict) or not isinstance(boosts.get("processed_messages"), list):
            raise ValueError("Formato antigo ou inválido em boosts.json; use um DATA_DIR vazio. O arquivo existente não foi alterado.")

    def read(self, name):
        with (self.data_dir / f"{name}.json").open(encoding="utf-8") as file:
            return json.load(file)

    def write(self, name, value):
        path = self.data_dir / f"{name}.json"
        fd, temporary = tempfile.mkstemp(dir=self.data_dir, prefix=f".{name}-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                json.dump(value, file, indent=2, ensure_ascii=False)
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    async def record_message(self, message_id, user_id):
        async with self.lock:
            data = self.read("boosts")
            message_id = str(message_id)
            if message_id in data["processed_messages"]:
                return None
            user_id = str(user_id)
            data["users"][user_id] = data["users"].get(user_id, 0) + 1
            data["processed_messages"].append(message_id)
            self.write("boosts", data)
            return data["users"][user_id]

    async def set_count(self, user_id, count):
        async with self.lock:
            data = self.read("boosts")
            data["users"][str(user_id)] = max(0, count)
            self.write("boosts", data)
            return data["users"][str(user_id)]

    def count(self, user_id):
        return self.read("boosts")["users"].get(str(user_id), 0)


async def setup(bot):
    await bot.add_cog(GestorDados(bot))
