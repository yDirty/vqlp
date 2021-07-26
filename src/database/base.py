import json
import typing as ty


class Location:

    """Использование базы данных.
    Конфигурация происходит из json формата под "database.json"
    Можно в ручную изменять данные в джсоне, к примеру <custom_prefixes>


    Также есть добавление данных json формата по методу add_object_the_database(
                                                     value: ty.Any,
                                                     method: str)
    :value Обьект, который будет сохранён в method.
    :method Обьект, который хранится в database.json
    100 строка данного файла.

    Использование данного класса в коде:

        from src.database.base import location

        @app.command("info", prefixes=['/'])  #/info
        async def wrapper(
                  ctx: vq.NewMessage) -> ty.Optional[str]:
            command_text = f'''
        Кол-во заметок: {len(location.notes)}
        Префиксы: {location.custom_prefixes}
        '''
            return command_text
    """

    notes: ty.List[dict]  # [{"name": "", "text": ""}]
    token: ty.Union[list, str]
    deleter_prefixes: ty.Dict[list, str]
    custom_prefixes: ty.List[str]
    role_plays_commands: ty.List[dict]
    trigger_prefixes: ty.List[str]
    ignore_list: ty.List[dict]
    muted_list: ty.List[dict]
    friend_ids: ty.List[int]

    auto_greeting: ty.Optional[str]
    auto_mine: ty.Any = None
    auto_commands: ty.Dict
    auto_leave_chat: ty.Any = None
    idm_secret_code: ty.Optional[str]
    idm_signal_prefixes: ty.List[str]
    idm: ty.Optional[dict]

    author = "ymoth"
    version: ty.Optional[str] = "1.0.0"

    def __init__(self) -> json.load:
        with open("database.json", encoding='utf-8') as opener_json_format:
            try:
                keys = json.load(opener_json_format)
                self.token = keys['token']
                self.deleter_prefixes = keys['deleter_prefixes']
                self.custom_prefixes = keys['custom_prefixes']
                self.role_plays_commands = keys['role_plays_commands']
                self.notes = keys['triggers_prefixes']
                self.idm_secret_code = keys['IDM']['secret_code_idm']
                self.trigger_prefixes = keys['triggers_prefixes']
                self.idm_signal_prefixes = keys['IDM']['signal_prefixes']
                self.ignore_list = keys['ignore_list']
                self.muted_list = keys['muted_list']
                self.auto_kicked_user = keys['auto_kicked_user']
                self.friend_ids = keys['friend_ids']
                self.auto_greeting = keys['auto_greeting']
                self.auto_leave_chat = keys['auto_commands']["auto_leave_chat"]
                self.auto_mine = keys['auto_commands']["auto_mine"]
                self.auto_commands = keys['auto_commands']
                self.idm = keys['IDM']
            except:
                ...

    def __call__(self, *args, **kwargs):
        with open("database.json", encoding='utf-8') as opener_json_format:
            keys = json.load(opener_json_format)
            self.token = keys['token']
            self.deleter_prefixes = keys['deleter_prefixes']
            self.custom_prefixes = keys['custom_prefixes']
            self.role_plays_commands = keys['rp_commands']
            self.notes = keys['triggers_prefixes']
            self.idm_secret_code = keys['IDM']['secret_code_idm']
            self.trigger_prefixes = keys['triggers_prefixes']
            self.idm_signal_prefixes = keys['IDM']['signal_prefixes']
            self.ignore_list = keys['ignore_list']
            self.muted_list = keys['muted_list']
            self.auto_kicked_user = keys['auto_kicked_user']
            self.friend_ids = keys['friend_ids']
            self.auto_greeting = keys['auto_greeting']
            self.auto_leave_chat = keys['auto_commands']["auto_leave_chat"]
            self.auto_mine = keys['auto_commands']["auto_mine"]
            self.auto_commands = keys['auto_commands']
            self.idm = keys['IDM']

    @staticmethod
    def add_object_the_database(method: ty.Optional[str], value: ty.Any):
        with open(f"database.json", "r", encoding="utf-8") as database:  # The loading database
            data = json.load(database)
        data[method] = value
        with open(f"database.json", "w", encoding="utf-8") as database:  # The save object the database
            database.write(json.dumps(data, indent=3, ensure_ascii=False))


location = Location()
