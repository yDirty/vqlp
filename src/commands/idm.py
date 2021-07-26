import asyncio
import typing as ty

import aiohttp
import vkquick as vq

from src.misc import app

from src.database.base import location
from src.config import error_sticker, complete_sticker
from src.filters.error_handler import ErrorHandler


@app.command("+идм префикс", invalid_argument_config=ErrorHandler())
async def add_prefix_idm(
        new_prefix: str
) -> ty.Optional[str]:
    prefixes = location.idm_signal_prefixes
    if new_prefix.strip() + ' ' in prefixes:
        return f"""У вас уже есть данный префикс для сигналов."""

    prefixes.append(new_prefix.strip() + ' ')
    location.add_object_the_database(value={
        "secret_code_idm": location.idm_secret_code,
        "signal_prefixes": prefixes
    }, method='IDM')
    return f"{complete_sticker} Поставлен новый идм префикс <<{new_prefix}>>"


@app.command("-идм префикс", invalid_argument_config=ErrorHandler())
async def add_prefix_idm(
        new_prefix: str
) -> ty.Optional[str]:
    prefixes = location.idm_signal_prefixes
    if new_prefix.strip() + ' ' not in prefixes:
        return f"""У вас нету данного префикса для сигналов."""

    prefixes.append(new_prefix.strip() + ' ')
    location.add_object_the_database(value={
        "secret_code_idm": location.idm_secret_code,
        "signal_prefixes": prefixes
    }, method='IDM')
    return f"{complete_sticker} Удалён идм префикс <<{new_prefix}>>"


@app.command("+секретка", invalid_argument_config=ErrorHandler())
async def add_secret_code_idm(
        ctx: vq.NewMessage,
        new_secret: ty.Optional[str]) -> None:
    if len(location.idm_secret_code) < 0:
        await ctx.reply(
            f"Ваш секретный код изменён на {new_secret}\nПрошлый секретный код: {location.idm_secret_code}")
        idm_sec_code = location.idm
        idm_sec_code["secret_code_idm"] = new_secret
        location.add_object_the_database(method='auto_commands', value=idm_sec_code)
        return

    await ctx.reply(
        f"Добавлен секретный код IDM.")
    idm_sec_code = location.idm
    idm_sec_code["secret_code_idm"] = new_secret
    location.add_object_the_database(method='IDM', value=idm_sec_code)


@app.command(*location.idm_signal_prefixes, prefixes=[''], invalid_argument_config=ErrorHandler())
async def call_command_for_idm(
        ctx: vq.NewMessage,
        *,
        signal: str = None
) -> str:
    await ctx.msg.extend(ctx.api)
    from_id_user = ctx.msg.from_id
    json_request = {
        "user_id": from_id_user,
        "secret": location.idm_secret_code,
        'method': 'lpSendMySignal',
        'message': {
            'conversation_message_id': ctx.msg.conversation_message_id,
            "from_id": from_id_user,
            "peer_id": ctx.msg.peer_id,
            "date": ctx.msg.date.timestamp(),
            "text": ctx.msg.text},
        'object': {
            'chat': None,
            'from_id': from_id_user,
            'value': ctx.msg.text,
            "conversation_message_id": ctx.msg.conversation_message_id},
        "vkmessage": {'id': ctx.msg.id, 'peer_id': ctx.msg.peer_id, 'is_win_platform': True}}

    print(json_request)
    duty_name = 'vqlp'
    async with aiohttp.ClientSession() as session:
        async with session.post('https://irisduty.ru/callback/', json=json_request) as resp:
            if resp.status != 200:
                message = f"{duty_name} | ⚠ Ошибка сервера IDM Multi. Сервер, ответил кодом {resp.status}."
            else:
                data_json = await resp.json()
                if data_json['response'] == 'ok':
                    return
                elif data_json['response'] == "error":
                    if data_json.get('error_code') == 1:
                        message = f"{duty_name} | ⚠ Ошибка сервера IDM Multi. Сервер, ответил: <<Пустой запрос>>"
                    elif data_json.get('error_code') == 2:
                        message = f'{duty_name} | ⚠ Ошибка сервера IDM Multi. Сервер, ответил: <<Неизвестный тип ' \
                                  f'сигнала>> '
                    elif data_json.get('error_code') == 3:
                        message = (
                            f"{duty_name} | ⚠ Ошибка сервера IDM Multi. "
                            f"{duty_name} | Сервер, ответил: <<Пара пользователь/секрет не найдены>>"
                        )
                    elif data_json.get('error_code') == 4:
                        message = f"{duty_name} | ⚠ Ошибка сервера IDM Multi. Сервер, ответил: <<Беседа не привязана>>"

                    elif data_json.get('error_code') == 10:
                        message = f'{duty_name} | ⚠ Ошибка сервера IDM Multi. Сервер, ответил: <<Не удалось связать ' \
                                  f'беседу>> '
                    else:
                        message = (
                            f"{duty_name} | ⚠ Ошибка сервера IDM Multi. "
                            f"{duty_name} | Сервер, ответил: <<Ошибка #{data_json.get('error_code')}>>"
                        )
                elif data_json['response'] == "vk_error":
                    message = (
                        f"⚠ Ошибка сервера IDM Multi. "
                        f"Сервер, ответил: "
                        f"<<Ошибка VK #{data_json.get('error_code')} {data_json.get('error_message', '')}>>"
                    )
        return message
