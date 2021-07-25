import vkquick as vq

from src.filters.only_me import OnlyMe
from src.misc import app


@app.command("пинг")
async def pinged():
    return "pong."
