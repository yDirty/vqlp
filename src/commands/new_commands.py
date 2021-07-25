import vkquick as vq

from src.misc import app


@app.command("хуй")
async def _(ctx: vq.NewMessage):
    await ctx.answer("111")
