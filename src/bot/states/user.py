from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    any_state = State()


class AdminState(StatesGroup):
    any_state = State()
