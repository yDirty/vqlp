import asyncio
import typing as ty

import vkquick as vq

from src.misc import app

from src.database.base import location
from src.config import error_sticker, complete_sticker


@app.command("+удалялка")
async def add_deleter(ctx: vq.NewMessage, *, new_prefix: str):
    """Added new prefix for delete messages"""
    prefixes: list = location.deleter_prefixes['prefixes']
    text_prefixes = location.deleter_prefixes['text_prefixes']
    if new_prefix.strip() in prefixes:
        return f"{error_sticker} У вас уже есть данный префикс <<{new_prefix}>>"

    prefixes.append(new_prefix.strip())
    location.add_object_the_database(value={
        "prefixes": prefixes,
        'text_prefixes': text_prefixes
    }, method='deleter_prefixes')
    return f"{complete_sticker} Вы добавили новый префикс <<{new_prefix}>> для удалялки." \
           f"Сработает после перезапуска."


@app.command("-удалялка")
async def delete_deleter(ctx: vq.NewMessage, *, old_prefix: str):
    """Added new prefix for delete messages"""
    prefixes: list = location.deleter_prefixes['prefixes']
    text_prefixes = location.deleter_prefixes['text_prefixes']
    if old_prefix.strip() not in prefixes:
        return f"{error_sticker} У вас нету есть данного префикса <<{old_prefix}>>"

    prefixes.remove(old_prefix.strip())
    location.add_object_the_database(value={
        "prefixes": prefixes,
        'text_prefixes': text_prefixes
    }, method='deleter_prefixes')
    return f"{complete_sticker} Вы добавили новый префикс <<{old_prefix}>> для удалялки." \
           f"Сработает после перезапуска."


@app.command(*location.deleter_prefixes['prefixes'], prefixes=[''])
async def delete_last_messages(
        ctx: vq.NewMessage, how_much: ty.Optional[str]) -> None:
    if not how_much:
        how_much = 10

    response = await ctx.api.messages.getHistory(
        peer_id=ctx.msg.peer_id,
        offset=0,
        count=200
    )
    response2 = await ctx.api.messages.getHistory(
        peer_id=ctx.msg.peer_id,
        offset=200,
        count=200
    )
    new_list = [*response['items'], *response2['items']]
    messages_ids_in_history = []
    for i in new_list:
        try:
            if len(messages_ids_in_history) < int(how_much):
                if i["from_id"] == ctx.msg.from_id:
                    messages_ids_in_history.append(i["id"])
                    await asyncio.sleep(0.3)
                    await ctx.api.messages.edit(
                        message_id=i['id'],
                        peer_id=ctx.msg.peer_id,
                        message=location.deleter_prefixes['text_prefixes'])
                    await ctx.api.messages.delete(message_ids=
                                                  messages_ids_in_history, delete_for_all=1)
        except:
            ...
