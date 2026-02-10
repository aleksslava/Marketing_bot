import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import DialogManager, StartMode, setup_dialogs

from amo_api.amo_api import AmoCRMWrapper
from dialogs.main_dialog import main_dialog

from handlers.start_handler import main_menu_router
from config.config import load_config
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from middleware.amo_api import AmoApiMiddleware
from middleware.app_script import AppScriptClient, AppScriptMiddleware

logger = logging.getLogger(__name__)

logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
logger.info("Starting Prosto_bot_2")


config = load_config()
storage = MemoryStorage()


bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher(storage=storage)
app_script = AppScriptClient(
    webhook_url=config.app_script.webhook_url,
    timeout_seconds=config.app_script.timeout_seconds,
    token=config.app_script.token,
)
amo_api = AmoCRMWrapper(
    path=config.amo_config.path_to_env,
    amocrm_subdomain=config.amo_config.amocrm_subdomain,
    amocrm_client_id=config.amo_config.amocrm_client_id,
    amocrm_redirect_url=config.amo_config.amocrm_redirect_url,
    amocrm_client_secret=config.amo_config.amocrm_client_secret,
    amocrm_secret_code=config.amo_config.amocrm_secret_code,
    amocrm_access_token=config.amo_config.amocrm_access_token,
    amocrm_refresh_token=config.amo_config.amocrm_refresh_token,
)

dp.update.middleware(AppScriptMiddleware(app_script))
dp.update.middleware(AmoApiMiddleware(amo_api, amo_fields=config.amo_fields))

dp.include_router(main_menu_router)
dp.include_routers(main_dialog)

setup_dialogs(dp)


if __name__ == '__main__':
    dp.run_polling(bot)
