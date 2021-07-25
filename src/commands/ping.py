import vkquick as vq

from src.misc import app


@app.command("пинг")
async def pinged(ctx: vq.NewMessage):
    return "pong."
