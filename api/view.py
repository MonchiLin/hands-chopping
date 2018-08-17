import flask
from flask_restful import Resource

import config
import data_spider.model as model

db = config.Config.db


class Game(Resource):
    def get(self):
        all = db.session.query(model.Game).get(1)
        return flask.jsonify(all)
