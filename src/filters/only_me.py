import vkquick as vq

from vkquick.chatbot.dependency import Depends
from vkquick.chatbot.storages import NewMessage


class OnlyMe(vq.BaseFilter):

    async def make_decision(self, ctx: NewMessage, **kwargs: Depends):
        if not ctx.msg.out:
            raise vq.StopCurrentHandling()

