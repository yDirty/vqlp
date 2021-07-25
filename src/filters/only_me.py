import vkquick as vq

from vkquick.chatbot.base.filter import BaseFilter
from vkquick.chatbot.dependency import Depends
from vkquick.chatbot.storages import NewMessage


class OnlyMe(BaseFilter):

    async def make_decision(self, ctx: NewMessage, **kwargs: Depends):
        if not ctx.msg.out:
            vq.StopCurrentHandling()
