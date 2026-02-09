from pathlib import Path
from dataclasses import dataclass
from environs import Env



BASE_DIR = Path(__file__).resolve().parent.parent



amo_fields = {
    'statuses': {},
    'pipelines': {}
}

# Класс с токеном бота телеграмм
@dataclass
class TgBot:
    token: str  #Токен для доступа к боту



# Класс с данными для подключения к API AMO
@dataclass
class AmoConfig:
    amocrm_subdomain: str
    amocrm_client_id: str
    amocrm_client_secret: str
    amocrm_redirect_url: str
    amocrm_access_token: str | None
    amocrm_refresh_token: str | None
    amocrm_secret_code: str
    path_to_env: str

@dataclass
class Config:
    tg_bot: TgBot
    amo_config: AmoConfig
    amo_fields: dict



# Функция создания экземпляра класса config
def load_config(path: str | None = BASE_DIR / '.env'):
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN")
        ),
        amo_config=AmoConfig(
            path_to_env=path,
            amocrm_subdomain=env("AMOCRM_SUBDOMAIN"),
            amocrm_client_id=env("AMOCRM_CLIENT_ID"),
            amocrm_client_secret=env("AMOCRM_CLIENT_SECRET"),
            amocrm_redirect_url=env("AMOCRM_REDIRECT_URL"),
            amocrm_access_token=env("AMOCRM_ACCESS_TOKEN"),
            amocrm_refresh_token=env("AMOCRM_REFRESH_TOKEN"),
            amocrm_secret_code=env("AMOCRM_SECRET")
        ),
        amo_fields=amo_fields,
    )