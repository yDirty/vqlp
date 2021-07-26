import asyncio
import typing as ty

import vkquick as vq

from src.misc import app

from src.database.base import location
from src.config import error_sticker, complete_sticker
from src.filters.error_handler import ErrorHandler


@app.on_message()
async def clear_function(ctx: vq.NewMessage) -> ty.Optional[None]:
    """Auto delete messages from ignored"""
    if ctx.msg.from_id in location.ignore_list:
        await ctx.api.messages.delete(
            message_id=ctx.msg.id,
            delete_for_all=0,
            peer_id=ctx.msg.peer_id
        )
