"""
Import modules
Framework the write bot: VKQuick.

Virtual Quarter Version: 1.0.7

Github: https://github.com/ymoth/vqlp
VKGroup: vk.com/vqlongpolling
"""

import asyncio
import sys

from loguru import logger

from src.database.base import location
from src.filters.other import check_access_token
from src.misc import app

logger.add(sys.stdout,
           format=f"[<yellow>Virtual Quarter</yellow>]" + " <blue>{"
                                                          "message}</blue> [{time:HH:mm:ss}]",
           level="INFO")


async def main():
    """Custom startup the Virtual Quarter

    Documentation: path <<autodocs>>. Html file.

    author: ymoth | VKQuick author: deknowny
    At the start, it is checked for the presence of a token.
    A separate function for testing is found in src.filters.other.

    The token can be transferred as a link or in other ways.
    Multiple tokens can be transferred.

    await app.coroutine_run ('token1', 'token2', 'token3')
    With the condition that you need to close the previous coroutine
    """

    if len(location.token) < 85:
        logger.opt(colors=True).info(
            "Ошибка конфига. Введите ваш <red>access_token</red>"
        )
        new_token = input("")
        response_token = check_access_token(new_token)
        if response_token['response']:
            location.add_object_the_database(
                value=response_token['token'],
                method='token'
            )
            user = response_token['user']['response'][0]
            logger.opt(colors=True).info(
                f"Приветствуем вас, <green>{user['first_name']} {user['last_name']}</green>\nОжидаем 3 секунды.")
            await asyncio.sleep(3)
            await app.coroutine_run(response_token['token'])
        else:
            logger.opt(colors=True).info(
                f"<red>{response_token['desc']}</green>"
            )
            return None
    else:
        try:
            # await app.coroutine_run('token1', 'token2', 'token3')
            await app.coroutine_run(location.token)
        except:
            logger.opt(colors=True).info("<red>Ошибка VK API! [5] Токен не действителен. ")
            return None


# Asyncio run the startup.
asyncio.run(main())
