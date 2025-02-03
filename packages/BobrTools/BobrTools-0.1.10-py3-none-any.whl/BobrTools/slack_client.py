
from .helpers import get_env_variable


class SlackClient:
    def __init__(self, token=None):
        self.token = token or get_env_variable("TELEGRAM_BOT_TOKEN")