import asyncio
import typing as ty

import vkquick as vq

from src.misc import app

from src.database.base import location
from src.config import error_sticker, complete_sticker
from src.filters.error_handler import ErrorHandler


@app.command("шаб", invalid_argument_config=ErrorHandler())
async def get_note(ctx: vq.NewMessage, name: str):
    if name not in [_['name_note'] for _ in location.notes]:
        return f"{error_sticker} У вас нет шаблона <<{name}>>"

    for i in location.notes:
        if i['name_note'] == name:
            await ctx.edit(i['message'], attachment=i['attachment'])


@app.command("рп", invalid_argument_config=ErrorHandler())
async def role_play_command(ctx: vq.NewMessage,
                            name_role: str,
                            user: vq.User) -> str:
    role_list = [role['name'] for role in location.role_plays_commands]
    if name_role.strip() not in role_list:
        return f"{error_sticker} У Вас нету данной команды."

    sticker = ''
    value_ = ''
    for v in location.role_plays_commands:
        if v['name'] == name_role.strip():
            sticker += v['sticker']
            value_ += v['value']
    _, i = await ctx.api.define_token_owner()
    await ctx.edit(
        f"{sticker} | {i:@[fullname]} {value_} {user:@[fullname]}")


@app.command("рпшки")
async def role_play_commands_get():
    """Get list for location.role_plays_commands"""
    text = f"""
Ваши рп-команды:
Стикер | Название | Действие
{''.join([f"{role['sticker']} | {role['name']} | {role['value']}<br>"
          for role in location.role_plays_commands])}
"""
    return text


@app.command("инфа")
async def get_information() -> str:
    text = f'''
Успешный стикер: {complete_sticker}
Еррор стикер: {error_sticker}    

Префиксы: {' | '.join([prefix for prefix in location.custom_prefixes])}
Триггер: {' | '.join([prefix for prefix in location.trigger_prefixes])}
Удалялки: {' | '.join([prefix for prefix in location.deleter_prefixes['prefixes']])}
Текст удалялки: {location.deleter_prefixes['text_prefixes']}

Шаблонов: {len(location.notes)}
РП-Команд: {len(location.role_plays_commands)}
Людей в игноре: {len(location.ignore_list)}
Доверенных: {len(location.friend_ids)}

IDM: {'Покдлючен' if len(location.idm_secret_code) < 0 else "Не подключен."}
IDM-Префиксы сигнала: {' | '.join([prefix for prefix in location.idm_signal_prefixes])}
Авто-команды:
Автоферма: {'Включена' if location.auto_mine else "Выключенна."}
Авто выход: {'Покдлючен' if location.auto_leave_chat else "Не подключен."}
'''
    return text
