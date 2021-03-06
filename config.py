import os
from enum import Enum, unique

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


class App(object):
    def __init__(self):
        pass

    @classmethod
    def get_app(cls, *args, **kwargs):
        if not hasattr(App, "_app"):
            App._app = Flask(__name__)
            App._app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///{}/data.db'.format(
                os.path.dirname(os.path.realpath(__file__)))
            App._app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
            App._app.config['CORS_HEADERS'] = 'Content-Type'
            CORS(App._app)
        return App._app

    @classmethod
    def get_db(cls, *args, **kwargs):
        if not hasattr(App, "_db"):
            App._db = SQLAlchemy(App.get_app())
        return App._db

    @classmethod
    def get_api(cls, *args, **kwargs):
        if not hasattr(App, "_api"):
            App._api = Api(App.get_app())
        return App._api


class Config:
    host = 'localhost'
    port = 6379
    sqlite = 'sqlite:///{}/data.db'.format(os.path.dirname(os.path.realpath(__file__)))
    path = os.path.dirname(os.path.realpath(__file__))
    img_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'img_dir')
    baseUrl = "https://store.playstation.com/"
    region = 'zh-hans-cn'
    app = App.get_app()
    api = App.get_api()
    db = App.get_db()
    timeZone = 'Asia/Shanghai'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36'}
    product = baseUrl + region + 'product'

    def __init__(self):
        self.links = []
        self.games = []

    def init_url(self, soup):
        links = soup.select('a.listItem')
        self.links = [{"link": link.attrs["href"], "title": link.text, "id": link.attrs["id"]} for link in links]


@unique
class Region(Enum):
    HK = 'zh-hant-hk'
    CHAIN = 'zh-hans-cn'

