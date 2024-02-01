from os import getenv
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


class Settings:
    """
    I prefer to use settings like in Django framework, so
        I've created this class and it's instance below
    Also I've applied the Singleton pattern to avoid creating
        new instances
    """

    _instance = None

    PG_NAME = getenv("PG_NAME")
    PG_USER = getenv("PG_USER")
    PG_PASSWORD = getenv("PG_PASSWORD")
    PG_PORT = getenv("PG_PORT") or 5432
    PG_HOST = getenv("PG_HOST") or "localhost"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance


settings = Settings()
