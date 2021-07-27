import asyncio
import typing as ty

import vkquick as vq

from src.misc import app

from src.database.base import location
from src.config import error_sticker, complete_sticker
from src.filters.error_handler import ErrorHandler

description_greeting = f"""
Авто-приветствие
Работает только на пользователей которые вошли в беседу
по ссылке.
Настройки: 
Text: {location.auto_greeting['text']} Value: {location.auto_greeting['value']}
"""


@app.command("удалялка", invalid_argument_config=ErrorHandler())
async def add_edit(*, data: str) -> ty.Optional[str]:
    location.add_object_the_database(value={"prefixes": location.deleter_prefixes['prefixes'],
                                            "text_prefixes": data}, method="deleter_prefixes")
    return f"{complete_sticker} Удалялка изменена на <<{data}>>"


@app.command("+дпрефикс", invalid_argument_config=ErrorHandler())
async def add_prefix(
        new_prefix: str):
    if new_prefix.strip() in location.trigger_prefixes:
        return f"{error_sticker} | У вас уже есть данный дпрефикс <<{new_prefix}>>"

    location.custom_prefixes.append(new_prefix.strip())
    location.add_object_the_database(method='trigger_prefixes', value=location.trigger_prefixes)
    return f"""{complete_sticker} Создан новый дпрефикс <<{new_prefix}>>."""


@app.command("-дпрефикс", invalid_argument_config=ErrorHandler())
async def add_prefix(
        old_prefix: str):
    if old_prefix not in location.trigger_prefixes:
        return f"{error_sticker} | У вас нету дпрефикса <<{old_prefix}>>"

    location.custom_prefixes.remove(old_prefix.strip() + ' ')
    location.add_object_the_database(method='trigger_prefixes', value=location.trigger_prefixes)
    return f"""{complete_sticker} Удалён дпрефикс <<{old_prefix}>>."""


@app.command("+дов", "вдов", invalid_argument_config=ErrorHandler())
async def add_friend(
        user: vq.User
) -> ty.Optional[str]:
    if user.id in location.friend_ids:
        return f"{error_sticker} | У вас уже есть {user:@[fullname]} в довах."

    location.friend_ids.append(user.id)
    location.add_object_the_database(value=location.friend_ids, method='friend_ids')
    return f"{complete_sticker} Пользователь {user:@[fullname]} успешно добавлен в довы."


@app.command("-дов", "издов", invalid_argument_config=ErrorHandler())
async def add_friend(
        user: vq.User
) -> ty.Optional[str]:
    if user.id not in location.friend_ids:
        return f"{error_sticker} | У вас нету {user:@[fullname]} в довах."

    location.friend_ids.remove(user.id)
    location.add_object_the_database(value=location.friend_ids, method='friend_ids')
    return f"{complete_sticker} Пользователь {user:@[fullname]} успешно убран из доверенных."


@app.command("+автокик", "в автокик", invalid_argument_config=ErrorHandler())
async def add_to_auto_kick_user(user: vq.User) -> ty.Optional[str]:
    if user.id in location.auto_kicked_user:
        return f"{error_sticker} Пользователь уже в авто-кике"

    location.auto_kicked_user.append(user.id)
    location.add_object_the_database(value=location.auto_kicked_user, method='auto_kicked_user')
    return f"{complete_sticker} {user:@[fullname]} Успешно добавлен в список авто-кика"


@app.command("-автокик", "из автокика", invalid_argument_config=ErrorHandler())
async def add_to_auto_kick_user(user: vq.User) -> ty.Optional[str]:
    if user.id not in location.auto_kicked_user:
        return f"{error_sticker} Пользователя нет в списке авто-кика"

    location.auto_kicked_user.remove(user.id)
    location.add_object_the_database(value=location.auto_kicked_user, method='auto_kicked_user')
    return f"{complete_sticker} {user:@[fullname]} Успешно убран из списка авто-кика"


@app.command("+приветствие", invalid_argument_config=ErrorHandler(), description=description_greeting)
async def add_greeting(*, text: str) -> ty.Optional[str]:
    location.add_object_the_database(value={'value': True, "text": text})
    return f"{complete_sticker} | Успешно включено приветствие, текст: {text}"


@app.command("-приветствие", invalid_argument_config=ErrorHandler())
async def delete_greeting() -> ty.Optional[str]:
    location.add_object_the_database(value={'value': False, "text": 'Close.'})
    return f"{complete_sticker} | Успешно выключено приветствие"


@app.command("+шаб", "+шаблон", invalid_argument_config=ErrorHandler())
async def add_note(
        ctx: vq.NewMessage,
        name: str,
        *,
        text: str
) -> ty.Optional[str]:
    base = [note['name_note'] for note in location.notes]
    if name in base:
        return f"{error_sticker} У вас уже есть шаблон с таким именем."

    attachments_all = []
    await ctx.msg.extend(ctx.api)
    fields = ctx.msg.fields
    for i in fields['attachments']:
        try:
            if i is None:
                ...
            else:
                attachments_all.append(f"{i['type']}{i[i['type']]['owner_id']}_{i[i['type']]['id']}")
        except:
            ...

    data_note = {
        "name_note": name,
        "message": text,
        "attachment": attachments_all if len(attachments_all) > 0 else None
    }
    location.notes.append(data_note)
    location.add_object_the_database(value=location.notes, method='notes')
    await ctx.edit(f"Вы успешно создали шаблон. Длина символов: {len(text)} | Вложений: {len(attachments_all)}")


@app.command("-шаб", '-шаблон', invalid_argument_config=ErrorHandler())
async def delete_note(name: str) -> ty.Optional[str]:
    base: list = [note['name_note'] for note in location.notes]
    if name not in base:
        return f"{error_sticker} У вас нету шаблона <<{name}>>"

    for i in location.notes:
        if i['name_note'] == name:
            location.notes.remove(i)

    return f"""{complete_sticker} Успешно удалён шаблон <<{name}>>"""


@app.command("+игнор")
async def add_for_ignore_user(user: vq.User) -> str:
    if user.id in location.ignore_list:
        return f"{error_sticker} Ошибка. Данный пользователь уже есть в игнор листе."
    location.ignore_list.append(user.id)
    location.add_object_the_database(value=location.ignore_list, method='ignore_list')
    return f"{complete_sticker} Пользователь {user:@[fullname]} был добавлен в игнор-лист"


@app.command("-игнор")
async def add_for_ignore_user(user: vq.User) -> str:
    if user.id not in location.ignore_list:
        return f"{error_sticker} Ошибка. Данного пользователя нет в игнор листе."

    location.ignore_list.remove(user.id)
    location.add_object_the_database(value=location.ignore_list, method='ignore_list')
    return f"{complete_sticker} Пользователь {user:@[fullname]} был убран из игнор-листа"


@app.command("+префикс", invalid_argument_config=ErrorHandler())
async def add_prefix(
        new_prefix: str):
    if new_prefix.strip() + ' ' in location.custom_prefixes:
        return f"{error_sticker} | У вас уже есть данный префикс <<{new_prefix}>>"

    location.custom_prefixes.append(new_prefix.strip() + ' ')
    location.add_object_the_database(method='custom_prefixes', value=location.custom_prefixes)
    return f"""{complete_sticker} Создан новый префикс <<{new_prefix}>>."""


@app.command("-префикс", invalid_argument_config=ErrorHandler())
async def add_prefix(
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
async def add_deleter(*, new_prefix: str):
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
async def delete_deleter(*, old_prefix: str):
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
