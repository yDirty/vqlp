import asyncio
import typing as ty

import vkquick as vq

from src.misc import app

from src.database.base import location
from src.config import error_sticker, complete_sticker
from src.filters.error_handler import ErrorHandler


@app.command("+игнор")
async def add_for_ignore_user(
        user: vq.User

) -> str:
    if user.id in location.ignore_list:
        return f"{error_sticker} Ошибка. Данный пользователь уже есть в игнор листе."
    user_ids = location.ignore_list.append(user.id)
    location.add_object_the_database(user_ids, 'ignore_list')
    return f"{complete_sticker} Пользователь {user:@[fullname]} был добавлен в игнор-лист"


@app.command("-игнор")
async def add_for_ignore_user(
        user: vq.User

) -> str:
    if user.id not in location.ignore_list:
        return f"{error_sticker} Ошибка. Данного пользователя нет в игнор листе."

    user_ids = location.ignore_list.remove(user.id)
    location.add_object_the_database(user_ids, 'ignore_list')
    return f"{complete_sticker} Пользователь {user:@[fullname]} был убран из игнор-листа"


@app.command("+префикс", invalid_argument_config=ErrorHandler())
async def add_prefix(ctx: vq.NewMessage,
                     new_prefix: str):
    if new_prefix.strip() + ' ' in location.custom_prefixes:
        return f"{error_sticker} | У вас уже есть данный префикс <<{new_prefix}>>"

    location.custom_prefixes.append(new_prefix.strip() + ' ')
    location.add_object_the_database(method='custom_prefixes', value=location.custom_prefixes)
    return f"""{complete_sticker} Создан новый префикс <<{new_prefix}>>."""


@app.command("-префикс", invalid_argument_config=ErrorHandler())
async def add_prefix(ctx: vq.NewMessage,
                     old_prefix: str):
    if old_prefix + ' ' not in location.custom_prefixes:
        return f"{error_sticker} | У вас нету префикса <<{old_prefix}>>"

    location.custom_prefixes.remove(old_prefix.strip() + ' ')
    location.add_object_the_database(method='custom_prefixes', value=location.custom_prefixes)
    return f"""{complete_sticker} Удалён префикс <<{old_prefix}>>."""


@app.command("+рп", 'добавить рп', invalid_argument_config=ErrorHandler(),
             description="+рп название стикер действие")
async def add_role_play(
        name_rp: str, sticker: str,
        *, value: str) -> str:
    roles = [role['name'] for role in location.role_plays_commands]
    if name_rp.strip() in roles:
        return f"{error_sticker} У вас уже есть рп-команда с таким названием"

    location.role_plays_commands.append(
        {"name": name_rp,
         "value": value,
         "sticker": sticker})

    location.add_object_the_database(value=location.role_plays_commands,
                                     method='role_plays_commands')
    return f"{complete_sticker} Вы создали рп команду <<{name_rp}>>"


@app.command("-рп", 'удалить рп', invalid_argument_config=ErrorHandler(), description="+рп название стикер действие")
async def delete_role_play(name_rp: str) -> str:
    roles = [role['name'] for role in location.role_plays_commands]
    if name_rp.strip() not in roles:
        return f"{error_sticker} У вас нету данной рп-команды."

    for i in location.role_plays_commands:
        if i['name'] == name_rp:
            location.role_plays_commands.remove(i)

    location.add_object_the_database(value=location.role_plays_commands,
                                     method='role_plays_commands')
    return f"{complete_sticker} Вы удалили рп команду <<{name_rp}>>"


@app.command("+удалялка", invalid_argument_config=ErrorHandler())
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


@app.command("-удалялка", invalid_argument_config=ErrorHandler())
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


@app.command(*location.deleter_prefixes['prefixes'], prefixes=[''], invalid_argument_config=ErrorHandler())
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
                    await ctx.api.messages.edit(
                        message_id=i['id'],
                        peer_id=ctx.msg.peer_id,
                        message=location.deleter_prefixes['text_prefixes'])
                    await ctx.api.messages.delete(message_ids=
                                                  messages_ids_in_history, delete_for_all=1)
                    await asyncio.sleep(0.1)
        except:
            ...
