from re import I
from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    RADIS_URL: str = os.getenv("RADIS_URL", "")
    AUTH0_DOMAIN: str = os.getenv("AUTH0_DOMAIN", "")
    AUDIENCE: str = os.getenv("AUDIENCE", "")
    ALGORITHMS: list[str] = os.getenv("ALGORITHMS", '["RS256"]').strip("[]").replace('"', "").split(",")


setting = Config()
