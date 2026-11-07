import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    token: str
    prefix: str


def load_config():
    token = os.getenv("TOKEN", "").strip()
    if not token:
        raise ValueError("Defina TOKEN no ambiente ou no arquivo .env")
    return Config(token=token, prefix=os.getenv("PREFIX", "bb."))


DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
