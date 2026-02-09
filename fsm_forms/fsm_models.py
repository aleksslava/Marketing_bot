from aiogram.filters.state import StatesGroup, State



class MainDialog(StatesGroup):
    main = State()
    switch = State()
    after_repair = State()
    before_repair = State()
    switch_kp = State()
    after_repair_kp = State()
    before_repair_kp = State()
    discount = State()
    when_call = State()
    later_message = State()
    connect_manager = State()
