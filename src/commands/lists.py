import asyncio
import typing as ty

import vkquick as vq

from src.misc import app

from src.database.base import location
from src.config import error_sticker, complete_sticker
from src.filters.error_handler import ErrorHandler


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


@app.command("мут лист", "в муте")
async def _(ctx: vq.NewMessage):
    text = []
    cul = 1
    users = await ctx.api.users.get(user_ids=location.muted_list)
    for i in users:
        cul += 0
        text.append(f"{cul}. @id{i['id']}({i['first_name']} {i['last_name']})\n")

    return f"{complete_sticker} Пользователи в муте: \n{' '.join(text)}"


@app.command("автокик лист", "в автокике")
async def _(ctx: vq.NewMessage):
    text = []
    cul = 0
    users = await ctx.api.users.get(user_ids=location.auto_kicked_user)
    for i in users:
        cul += 0
        text.append(f"{cul}. @id{i['id']}({i['first_name']} {i['last_name']})\n")

    return f"{complete_sticker} Автокик пользователи: \n{' '.join(text)}"


@app.command("шабы", "шаблоны")
async def _():
    text = []
    cul = 0
    for i in location.notes:
        cul += 1
        text.append(f"{cul}. {i['name_note']} | ")
    return f"{complete_sticker} Шаблоны: \n{' '.join(text)}"


@app.command("игнор лист", "игнорируемы")
async def _(ctx: vq.NewMessage):
    text = []
    cul = 0
    users = await ctx.api.users.get(user_ids=location.ignore_list)
    for i in users:
        cul += 0
        text.append(f"{cul}. @id{i['id']}({i['first_name']} {i['last_name']})\n")

    return f"{complete_sticker} Игнорируемые пользователи: \n{' '.join(text)}"
