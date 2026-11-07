import asyncio
import json

from cogs.gestor import GestorDados


def test_messages_are_deduplicated_and_survive_restart(tmp_path):
    async def run():
        store = GestorDados(None, tmp_path)
        assert await store.record_message(100, 42) == 1
        assert await store.record_message(100, 42) is None
        assert await store.record_message(101, 42) == 2
        restored = GestorDados(None, tmp_path)
        assert restored.count(42) == 2
        assert await restored.record_message(101, 42) is None
        assert await restored.set_count(42, 0) == 0
        assert await restored.record_message(100, 42) is None
    asyncio.run(run())


def test_initial_files_are_empty_and_valid(tmp_path):
    store = GestorDados(None, tmp_path)
    assert store.read("boosts") == {"users": {}, "processed_messages": []}
    assert json.loads((tmp_path / "admins.json").read_text()) == {"role_ids": []}
    assert store.read("config") == {}
