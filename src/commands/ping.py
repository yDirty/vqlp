import vkquick as vq

from src.filters.error_handler import ErrorHandler
from src.filters.only_me import OnlyMe
from src.misc import app


@app.command("пинг", invalid_argument_config=ErrorHandler())
async def pinged():
    return "pong."
