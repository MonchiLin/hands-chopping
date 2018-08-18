from api import view
from config import Config


def create_app():
    return Config.app
