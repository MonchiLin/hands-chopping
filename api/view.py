from flask import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy import desc

import config
import data_spider.model as model

db = config.Config.db


class GameList(Resource):
    def get(self, page=None, per_page=None):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=50)
        args = parser.parse_args()
        page = page or args.page
        per_page = per_page or args.per_page

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
        if keyword is None or keyword.strip() == '':
            return GameList().get(1, 50)

        # keyword = r'%' + keyword + '%'

        raw_sql = r"SELECT * FROM game WHERE game_name LIKE '%{0}%' OR game_quanpin LIKE '%{0}%' OR game_jianpin LIKE '%{0}%'".format(
            keyword)

        # result = db.session.query(model.Game).filter(model.Game.game_name.like(keyword)).filter(
        #     model.Game.game_jianpin.like(keyword)).filter(
        #     model.Game.game_quanpin.like(keyword)).all()

        results = db.session.execute(raw_sql).fetchall()

        return jsonify(raw_query_to_json(results))


class Game(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('game_number', type=str, default=None)
        args = parser.parse_args()
        game_number = args.game_number

        if game_number is None:
            return

        # result = model.Price.query.filter_by(game_id=game_number).order_by(desc(model.Price.time)).all()
        game = model.Game.query.filter_by(game_number=game_number).first()
        prices = model.Price.query.filter_by(game_id=game.id).order_by(desc(model.Price.time)).all()

        return jsonify({
            'game': game.serialize,
            'prices': [p.serialize for p in prices]
        })


def convert_to_dict(results):
    temp = []
    for (key, value) in enumerate(results):
        obj = {}
        for k, v in enumerate(value._fields):
            obj[v] = value[k]
        temp.append(obj)
    return temp


def raw_query_to_json(results):
    d, a = {}, []
    for rowproxy in results:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d = {**d, **{tup[0]: tup[1]}}
        a.append(d)
    return a
