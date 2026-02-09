import asyncio
import datetime
import logging
from dis import show_code

from aiogram import F
from aiogram.enums import ContentType, ParseMode
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Column, Back, SwitchTo, Url
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window, DialogManager, StartMode, ShowMode
from lexicon.lexicon import urls
from config.config import BASE_DIR
from fsm_forms.fsm_models import MainDialog
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from amo_api.amo_api import AmoCRMWrapper
from aiogram.utils.chat_action import ChatActionSender


logger = logging.getLogger(__name__)

async def switch(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.switch)

async def after_repair(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.after_repair)

async def before_repair(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.before_repair)

async def start_message_getter(dialog_manager: DialogManager, **kwargs):
    first_name = dialog_manager.event.from_user.first_name
    return {'first_name': first_name}

start_window = Window(
    Format('<b>{first_name} здравствуйте!</b>\n\n'
          'На связи беспроводной умный дом HiTE PRO и умные замки KEYWAY.\n'
          'Какая инструкция вас интересует?'),
    Column(
        Button(Const('Беспроводные радиовыключатели'), id ='1', on_click=switch),
        Button(Const(' Умный дом после ремонта'), id ='2', on_click=after_repair),
        Button(Const('Умный дом до ремонта'), id ='3', on_click=before_repair),
    ),
    state=MainDialog.main,
    getter=start_message_getter,
)
async def switch_to_kp(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.switch_kp, show_mode=ShowMode.SEND)

async def after_to_kp(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.after_repair_kp, show_mode=ShowMode.SEND)

async def before_to_kp(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.before_repair_kp, show_mode=ShowMode.SEND)

switch_window = Window(
    Const('Отправляем вам краткую инструкцию👇🏻\n\n'
          'Установка беспроводного выключателя занимает 15 минут.\n'
          'А беспроводной умный свет можно добавить как до, так и после ремонта за 1 день.\n'
          'Устройства работают по радиоканалу, без интернета на расстоянии до 250 кв.м.\n\n'
          'Узнать подробнее и посмотреть полный ассортимент можно на нашем сайте hite-pro.ru\n\n'
          'Мы также можем подобрать вам установщика в любом городе России и даем гарантию 3 года 🇷🇺'),
    StaticMedia(
        path=BASE_DIR / "media" / "photo" / "switch_instr.jpg",
        type=ContentType.PHOTO,
    ),
    Button(Const('Далее'), id='1', on_click=switch_to_kp),
    state=MainDialog.switch,
)

after_repeir_window = Window(
    Const('Отправляем вам краткую инструкцию👇🏻\n\n'
          'Установка беспроводного выключателя занимает 15 минут.\n'
          'А беспроводной умный свет можно добавить как до, так и после ремонта за 1 день.\n'
          'Устройства работают по радиоканалу, без интернета на расстоянии до 250 кв.м.\n\n'
          'Узнать подробнее и посмотреть полный ассортимент можно на нашем сайте hite-pro.ru\n\n'
          'Мы также можем подобрать вам установщика в любом городе России и даем гарантию 3 года 🇷🇺'),
    StaticMedia(
        path=BASE_DIR / "media" / "photo" / "after_repair_instr.jpg",
        type=ContentType.PHOTO,
    ),
    Button(Const('Далее'), id='1', on_click=after_to_kp),
    state=MainDialog.after_repair,
)

before_repair_window = Window(
    Const('Отправляем вам краткую инструкцию👇🏻\n\n'
          'Установка беспроводного выключателя занимает 15 минут.\n'
          'А беспроводной умный свет можно добавить как до, так и после ремонта за 1 день.\n'
          'Устройства работают по радиоканалу, без интернета на расстоянии до 250 кв.м.\n\n'
          'Узнать подробнее и посмотреть полный ассортимент можно на нашем сайте hite-pro.ru\n\n'
          'Мы также можем подобрать вам установщика в любом городе России и даем гарантию 3 года 🇷🇺'),
    StaticMedia(
        path=BASE_DIR / "media" / "photo" / "before_repair_instr.jpg",
        type=ContentType.PHOTO,
    ),
    Button(Const('Далее'), id='1', on_click=before_to_kp),
    state=MainDialog.before_repair,
)

async def to_discount(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.discount)

switch_kp_window = Window(
    Const('Прикрепляем типовой расчет для 2-х комнатной квартиры.\n\n'
          'Точная стоимость комплекта зависит от особенностей проектирования для ваших задач.'),
    StaticMedia(
        path=BASE_DIR / "media" / "photo" / "switch_kp.jpg",
        type=ContentType.PHOTO,
    ),
    Button(Const('Далее'), id='1', on_click=to_discount),
    state=MainDialog.switch_kp,
)

after_repair_kp_window = Window(
    Const('Прикрепляем типовой расчет для 2-х комнатной квартиры.\n\n'
          'Точная стоимость комплекта зависит от особенностей проектирования для ваших задач.'),
    StaticMedia(
        path=BASE_DIR / "media" / "photo" / "after_repair_kp.jpg",
        type=ContentType.PHOTO,
    ),
    Button(Const('Далее'), id='1', on_click=to_discount),
    state=MainDialog.after_repair_kp,
)

before_repair_kp_window = Window(
    Const('Прикрепляем типовой расчет для 2-х комнатной квартиры.\n\n'
          'Точная стоимость комплекта зависит от особенностей проектирования для ваших задач.'),
    StaticMedia(
        path=BASE_DIR / "media" / "photo" / "before_repair_kp.jpg",
        type=ContentType.PHOTO,
    ),
    Button(Const('Далее'), id='1', on_click=to_discount),
    state=MainDialog.before_repair_kp,
)

async def later(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.when_call, show_mode=ShowMode.SEND)

async def connect_with_manager(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.connect_manager)

discount_window = Window(
    Const('Дарим скидку 10% на любые модели беспроводных выключателей и устройства для умного дома!\n'
          'Скидка действительна в течение 3 дней.\n'
          ' Хотите получить индивидуальный расчет под ваш проект?'),
    Column(
        Button(Const('Да, хочу узнать прямо сейчас!'), id='1', on_click=connect_with_manager),
        Button(Const('Да, свяжитесь со мной позже.'), id='2', on_click=later),
    ),
    state=MainDialog.discount,
)

async def weekend_call_message(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.later_message)

async def end_month_call_message(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.later_message)

async def dont_know_call_message(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainDialog.later_message)

when_call_window = Window(
    Const('Когда вы хотите подобрать комплект?'),
    Column(
        Button(Const('На выходных'), id='1', on_click=weekend_call_message),
        Button(Const('В конце месяца'), id='2', on_click=end_month_call_message),
        Button(Const('Пока не знаю'), id='3', on_click=dont_know_call_message),
    ),
    state=MainDialog.when_call,
)
async def urls_get(dialog_manager: DialogManager, **kwargs):
    return {
        'forum': urls.get('forum'),
        'roznica': urls.get('roznica'),
    }
later_call_message_window = Window(
    Const('Хорошо, свяжемся с вами позже!\n\n'
          'А пока можете подписаться на наш телеграм-канал,\n'
          ' в нем мы делимся интересными кейсами по применению'
          ' беспроводного умного дома и последними новостями о наших разработках.'),
    Url(Const('🔵 Телеграмм канал'), url=Format("{forum}")),
    state=MainDialog.later_message,
    getter=urls_get,
)

connect_manager_window = Window(
    Const('👇Отлично! Пожалуйста, перейдите в чат с менеджером👇'),
    Url(Const('🔵 Перейти в чат'), url=Format("{roznica}")),
    state=MainDialog.connect_manager,
    getter=urls_get,

)

main_dialog = Dialog(start_window, switch_window, after_repeir_window, before_repair_window, switch_kp_window,
                     after_repair_kp_window, before_repair_kp_window, later_call_message_window, discount_window,
                     when_call_window, connect_manager_window)