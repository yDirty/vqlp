import typing as ty

import vkquick as vq

from src.filters.error_handler import ErrorHandler
from src.filters.none_class import Clear
from src.misc import app

from src.database.base import location


@app.on_message()
async def clear_function(ctx: vq.NewMessage) -> ty.Optional[None]:
    """Auto delete messages from ignored"""
    if ctx.msg.from_id in location.ignore_list:
        await ctx.api.messages.delete(
            message_id=ctx.msg.id,
            delete_for_all=0,
            peer_id=ctx.msg.peer_id
        )


@app.on_user_joined_by_link()
async def hello(ctx: vq.NewMessage) -> None:
    if location.auto_greeting['value']:
        await ctx.answer(location.auto_greeting['text'])


@app.on_added_page()
async def added(ctx: vq.NewMessage, new_page: vq.PageID, invite: vq.UserID):
    if invite in location.auto_kicked_user:
        await ctx.api.messages.removeChatUser(chat_id=ctx.msg.chat_id,
                                              user_id=invite)


@app.on_user_joined_by_link()
async def added(ctx: vq.NewMessage, invite: vq.UserID):
    if invite in location.auto_kicked_user:
        await ctx.api.messages.removeChatUser(chat_id=ctx.msg.chat_id,
                                              user_id=invite)


@app.command('повтори', prefixes=location.trigger_prefixes,
             invalid_argument_config=ErrorHandler(), filter=None)
async def hello_(ctx: vq.NewMessage, *, message: str):
    if ctx.msg.from_id in location.friend_ids:
        await ctx.answer(message)
