from flask import jsonify
from flask_restful import Resource, reqparse

import config
import data_spider.model as model

db = config.Config.db


class GameList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=50)
        args = parser.parse_args()
        page = args.page
        per_page = args.per_page

        games = model.Game.query.with_entities(model.Game.id, model.Game.game_name, model.Game.game_number,
                                               model.Game.game_link).paginate(page, per_page, error_out=False)

        games.items = convert_to_dict(games.items)

        for index, game in enumerate(games.items):
            game_id = game['id']
            data = db.session.query(model.Price).filter(model.Price.game_id == game_id).all()

            game["game_price"] = data[-1].game_price

        data = {
            'items': games.items,
            'page': games.page,
            'per_page': games.per_page,
            'total': games.total,
            'pasge': games.pages,
        }
        return jsonify(data)


class PriceList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=50)
        args = parser.parse_args()
        page = args.page
        per_page = args.per_page

        prices = db.session.query(model.Price).with_entities(model.Price.id, model.Price.game_id,
                                                             model.Price.game_price,
                                                             model.Price.time).distinct(
            model.Price.game_price).order_by(model.Price.game_price).paginate(page, per_page, error_out=False)
        prices.items = convert_to_dict(prices.items)
        data = {
            'items': prices.items,
            'page': prices.page,
            'per_page': prices.per_page,
            'total': prices.total,
            'pasge': prices.pages,
        }
        return jsonify(data)


class Filter(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str, default=None)
        args = parser.parse_args()
        keyword = args.keyword
        if keyword is None:
            return []

        result = db.session.query(model.Game).filter(model.Game.game_name.like(keyword)).filter(
            model.Game.game_jianpin.like(keyword)).filter(
            model.Game.game_quanpin.like(keyword)).all()

        print(result)

        return []


def convert_to_dict(results):
    temp = []
    for (key, value) in enumerate(results):
        obj = {}
        for k, v in enumerate(value._fields):
            obj[v] = value[k]
        temp.append(obj)
    return temp
