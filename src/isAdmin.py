from aiogram.filters import Filter
from aiogram.types import Message

class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        # not_allowed = set(message.text) - self.allowed_characters
        # return len(not_allowed) == 0
        return message.from_user.id==5796548542