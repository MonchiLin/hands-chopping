from flask import jsonify
from flask_restful import Resource

import config
import data_spider.model as model

db = config.Config.db


class GameList(Resource):
    def get(self):
        game = model.Game.query.with_entities(model.Game.id, model.Game.game_name, model.Game.game_number,
                                              model.Game.gama_link).all()
        return jsonify(convert_to_dict(game))


class PriceList(Resource):
    def get(self):
        prices = db.session.query(model.Price).with_entities(model.Price.id, model.Price.game_id,
                                                             model.Price.gama_price,
                                                             model.Price.time).distinct(
            model.Price.gama_price).all()
        return jsonify(convert_to_dict(prices))


def convert_to_dict(results):
    temp = []
    for (key, value) in enumerate(results):
        obj = {}
        for k, v in enumerate(value._fields):
            obj[v] = value[k]
        temp.append(obj)
    return temp
