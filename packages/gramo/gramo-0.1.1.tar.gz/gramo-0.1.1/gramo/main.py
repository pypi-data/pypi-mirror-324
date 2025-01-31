from typing import Any, Dict, Optional, Callable
import requests, re

class MemoryStorage:
    def __init__(self, default_values: dict = None):
        """Initialize session storage and set default values."""
        self.sessions = {}
        self.default_values = default_values or {}

    def execute(self, default_values):
        return MemoryStorage(default_values)

    def get(self, user_id: int, key: str) -> any:
        """Retrieve a value from the session. If it doesn't exist, return the default."""
        if user_id not in self.sessions:
            self.sessions[user_id] = {}
        
        if key not in self.sessions[user_id]:
            if key in self.default_values:
                self.sessions[user_id][key] = self.default_values[key]
            else:
                self.sessions[user_id][key] = None
        
        return self.sessions[user_id][key]

    def set(self, user_id: int, key: str, value: any) -> None:
        if user_id not in self.sessions:
            self.sessions[user_id] = {}
        self.sessions[user_id][key] = value

    def delete(self, user_id: int, key: str) -> None:
        if user_id in self.sessions and key in self.sessions[user_id]:
            del self.sessions[user_id][key]

    def clear(self, user_id: int) -> None:
        if user_id in self.sessions:
            self.sessions[user_id] = {}


class DeepGetter:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data
    
    def __getattr__(self, name: str) -> str | int | bool | Any:
        if name in self.data:
            value = self.data[name]
            if isinstance(value, dict):
                return DeepGetter(value)
            return value
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __getitem__(self, key: str) -> Any:
        value = self.data.get(key, None)
        if isinstance(value, dict):
            return DeepGetter(value)
        return value

class Composer:

    def __init__(self):
        self.handlers = {}

    def command(self, command: str):
        def decorator(func: Callable):
            self.handlers[func.__name__] = {
                "type": "command",
                "function": func,
                "payload": command
            }

            return func

        return decorator
    
    def hears(self, regex: str) -> Callable:
        def decorator(func: Callable):
            self.handlers[func.__name__] = {
                "type": "hears",
                "function": func,
                "payload": regex
            }
            
            return func

        return decorator
    
    def middleware(self, *args):
        def decorator(func: Callable):
            return func
        
        return decorator
    
    def use(self, composer):
        self.handlers.update(composer.handlers)
    
class Message(DeepGetter):
    def __init__(self, data, match):
        self.match = match
        super().__init__(data)

class Context:

    def __init__(self, message: dict, endpoint: str, session: MemoryStorage):
        self.message = message
        self.endpoint = endpoint
        self.chat_id = message.get("chat", {}).get("id")
        self.text = message.get('text')
        self.session: MemoryStorage = session

    def reply(self, text: str):
        response = requests.post(f"{self.endpoint}/sendMessage", data={
            "chat_id": self.chat_id,
            "text": text
        })

        return response.json()

class Gramo(Composer):

    def __init__(self, bot_token: str, plugins: list):
        # self.session_name = session_name
        # self.api_id = api_id
        # self.api_hash = api_hash
        self.bot_token = bot_token
        self.endpoint = f"https://api.telegram.org/bot{bot_token}"

        self.load_plugins(plugins)

        super().__init__()

    def load_plugins(self, plugins):
        for plugin in plugins:
            self.session = plugin

    def handle_update(self, update: dict):
        message: dict = update.get("message")
        if message:
            text: str = message.get("text")
            chat_id:dict = message.get("chat", {}).get("id")

            message['from_user'] = message['from']
            del message['from']

            for _ in self.handlers:

                handler = self.handlers[_]
                func = None
                match = None
                
                if text and text.startswith("/") and handler['type'] == "command" and text[1:] == handler['payload']:
                    func = handler['function']
                elif text and handler['type'] == 'hears' and re.match(handler['payload'], text):
                    func = handler['function']
                    match = re.match(handler['payload'], text).groups()

                if func is None: continue

                func(Context(message, self.endpoint, self.session), Message(message, match))
                return

    def get_updates(self, offset=None):
        response = requests.get(f"{self.endpoint}/getUpdates", params= {
            "offset": offset
        } if offset else {})

        return response.json()

    def start_polling(self):
        offset = None
        while True:
            updates: dict = self.get_updates(offset)

            for update in updates.get("result", []):
                self.handle_update(update)
                offset = update["update_id"] + 1