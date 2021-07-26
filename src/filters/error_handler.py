from vkquick.chatbot.base.cutter import InvalidArgumentConfig

from src import config


class ErrorHandler(InvalidArgumentConfig):
    prefix_sign: str = config.error_sticker
    invalid_argument_template: str = (
        "{prefix_sign} vqlp | Некорректное значение "
        "`{incorrect_value}`. Необходимо передать {cutter_description}"
    )
    laked_argument_template: str = (
        "{prefix_sign} vqlp | Необходимо передать {cutter_description}"
    )
