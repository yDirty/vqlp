from src.misc import app
from src.filters.other import check_access_token


@app.on_startup()
async def wrapper(_):
    ...
