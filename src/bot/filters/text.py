from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from utils import get_text_button


class GetTextButton(Filter):
    def __init__(self, name: str) -> None:
        self.name = name

    async def __call__(self, message: Message) -> bool:
        return message.text == await get_text_button(self.name)


class FilterStrByIndex(Filter):
    def __init__(self, compare: str, index: int = -1, sep: str = ":") -> None:
        self.compare = compare
        self.index = index
        self.sep = sep

    async def __call__(
        self,
        query: CallbackQuery,
    ) -> bool:
        return query.data.split(self.sep)[self.index] == self.compare
