from flask import jsonify
from flask_restful import Resource

import config
import data_spider.model as model

db = config.Config.db


class GameList(Resource):
    def get(self, page=0, per_page=50):
        game = model.Game.query.with_entities(model.Game.id, model.Game.game_name, model.Game.game_number,
                                              model.Game.gama_link).paginate(page, per_page, error_out=False)
        game.items = convert_to_dict(game.items)
        data = {
            'items': game.items,
            'page': game.page,
            'per_page': game.per_page,
            'total': game.total,
            'pasge': game.pages,
        }
        return jsonify(data)


class PriceList(Resource):
    def get(self):
        return self.post(0, 50)

    def post(self, page=0, per_page=50):
        prices = db.session.query(model.Price).with_entities(model.Price.id, model.Price.game_id,
                                                             model.Price.gama_price,
                                                             model.Price.time).distinct(
            model.Price.gama_price).order_by(model.Price.gama_price).paginate(page, per_page, error_out=False)
        prices.items = convert_to_dict(prices.items)
        data = {
            'items': prices.items,
            'page': prices.page,
            'per_page': prices.per_page,
            'total': prices.total,
            'pasge': prices.pages,
        }
        return jsonify(data)


def convert_to_dict(results):
    temp = []
    for (key, value) in enumerate(results):
        obj = {}
        for k, v in enumerate(value._fields):
            obj[v] = value[k]
        temp.append(obj)
    return temp
