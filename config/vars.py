import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DOUBLEBOOSTER_ID = int(os.getenv("DOUBLEBOOSTER_ID", "0"))
CANAL_ID = int(os.getenv("CANAL_ID", "0"))
DIRETORIO_BOOSTS = "data/boosts.json"
