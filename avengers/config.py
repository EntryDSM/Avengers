import os

import hvac

VAULT_ADDRESS = "https://vault.entrydsm.hs.kr"
SERVICE_NAME = os.environ.get("SERVICE_NAME")

VAULT_TOKEN = os.environ.get("VAULT_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

RUN_ENV = os.environ.get("RUN_ENV")

LOGO = """
──────────────▐█████───────
──────▄▄████████████▄──────
────▄██▀▀────▐███▐████▄────
──▄██▀───────███▌▐██─▀██▄──
─▐██────────▐███─▐██───██▌─
─██▌────────███▌─▐██───▐██─
▐██────────▐███──▐██────██▌
██▌────────███▌──▐██────▐██
██▌───────▐███───▐██────▐██
██▌───────███▌──▄─▀█────▐██
██▌──────▐████████▄─────▐██
██▌──────█████████▀─────▐██
▐██─────▐██▌────▀─▄█────██▌
─██▌────███─────▄███───▐██─
─▐██▄──▐██▌───────────▄██▌─
──▀███─███─────────▄▄███▀──
──────▐██▌─▀█████████▀▀────
──────███──────────────────                                                
"""


class VaultClient:
    _database_credential = None

    @classmethod
    def initialize(cls):
        cls.client = hvac.Client(url=VAULT_ADDRESS)

        if VAULT_TOKEN:
            cls.client.token = VAULT_TOKEN
        elif GITHUB_TOKEN:
            cls.client.auth.github.login(token=GITHUB_TOKEN)

    def __getattr__(self, item):
        try:
            data = self.client.read(
                f"service-secret/{RUN_ENV}/{SERVICE_NAME}"
            )["data"]
            return data[item]
        except (KeyError, TypeError):
            raise Exception(f"request on: service-secret/{RUN_ENV}/{SERVICE_NAME} \nrequested key {item} is can't be fetched")
        except Exception as e:
            raise e


class Setting:
    def __init__(self, vault_client: VaultClient):
        self.vault_client = vault_client

    def __getattr__(self, item):
        return self.vault_client.__getattr__(item)

    @property
    def database_connection_info(self):
        return {
            "use_unicode": True,
            "charset": "utf8mb4",
            "user": self.vault_client.MYSQL_USERNAME,
            "password": self.vault_client.MYSQL_PASSWORD,
            "db": self.vault_client.MYSQL_DATABASE,
            "host": self.vault_client.MYSQL_HOST,
            "port": self.vault_client.MYSQL_PORT,
            "loop": None,
            "autocommit": True,
        }

    @property
    def cache_connection_info(self):
        return {
            "address": f"redis://:{self.vault_client.REDIS_PASSWORD}@{self.vault_client.REDIS_HOST}:{self.vault_client.REDIS_PORT}",
            # pylint: disable=line-too-long
            "minsize": 5,
            "maxsize": 10,
        }

    DEBUG = False if RUN_ENV == "prod" else True


settings = Setting(VaultClient())  # pylint: disable=invalid-name
