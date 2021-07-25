import json
import typing as ty


class Location:
    """The database is in the path database.json category
    All objects are taken from there for convenient work
    """
    notes: ty.List[dict]  # [{"name": "", "text": ""}]
    token: ty.Union[list, str]
    deleter_prefixes: ty.List[dict]
    custom_prefixes: ty.List[str]
    role_plays_commands: ty.List[str]
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
        """Set self.object the using for function
        example:
            def wrapper(db: Location):
                my_token = db.token
                print(my_token)

            wrapper(DataJSON())

        or:
            def wrapper():
                db = Location()
                my_token = db.token
                print(my_token)

            wrapper()
        """
        with open("database.json", encoding='utf-8') as opener_json_format:
            try:
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
