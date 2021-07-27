import vkquick as vq

from vkquick.chatbot.dependency import Depends
from vkquick.chatbot.storages import NewMessage


class Clear(vq.BaseFilter):

    async def make_decision(self, ctx: NewMessage, **kwargs: Depends):
        raise vq.StopCurrentHandling()
