import vkquick as vq

from src.config import complete_sticker, error_sticker
from src.filters.error_handler import ErrorHandler
from src.misc import app
from src.database.base import location


@app.command("+др", invalid_argument_config=ErrorHandler())
async def friend_add(ctx: vq.NewMessage, user: vq.User):
    try:
        method = await ctx.api.friends.add(user_id=user.id)
        await ctx.edit(f"{complete_sticker} Выполнение...")
        if method == 1:
            await ctx.edit(f"{complete_sticker} Заявка в друзья отправлена пользователю {user:@[fullname]} отправлена.")
        elif method == 2:
            await ctx.edit(f"{complete_sticker} Заявка на добавление в друзья от {user:@[fullname} одобрена.")
        elif method == 4:
            await ctx.edit(f"{error_sticker} Повторная отправка заявки.")
    except vq.APIError[vq.CODE_174_FRIENDS_ADD_YOURSELF]:
        await ctx.edit(f"{error_sticker} Невозможно добавить в друзья самого себя.")


@app.command("-др", invalid_argument_config=ErrorHandler())
async def friend_delete(ctx: vq.NewMessage, user: vq.User):
    try:
        method = await ctx.api.friends.delete(user_id=user.id)
        await ctx.edit(f"{complete_sticker} Выполнение...")
        if method['success']:
            await ctx.edit(f"{complete_sticker} {user:@[fullname]} удален из списка друзей.")
        elif method['out_request_deleted']:
            await ctx.edit(f"{complete_sticker}Отменена исходящая заявка в друзья от пользователя {user:@[fullname]}")
        elif method['in_request_deleted']:
            await ctx.edit(f"{complete_sticker}Отклонена входящая заявка в друзья от пользователя {user:@[fullname]}")
    except:
        await ctx.edit("Пользователя нету в друзьях.")


@app.command("ид", invalid_argument_config=ErrorHandler())
async def revolve_user(ctx: vq.NewMessage, user: vq.User):
    await ctx.edit(f"✅Айди пользователя {user.fullname}: [id{user.id}|{user.id}]")


@app.command("влс", invalid_argument_config=ErrorHandler())
async def send_message(ctx: vq.NewMessage, user: vq.User, *, text: str):
    await ctx.api.messages.send(
        user_id=user.id,
        random_id=0,
        message=text
    )
    await ctx.edit(f"✅ Сообщение было отправлено пользователю : {user:@[fullname]}")
