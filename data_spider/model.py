import datetime

from config import Config

db = Config.db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.String, unique=True)
    game_name = db.Column(db.String)
    game_price = db.relationship('Price', backref='game', lazy='dynamic')
    game_link = db.Column(db.String)
    game_jianpin = db.Column(db.String, default='')
    game_quanpin = db.Column(db.String, default='')

    def __init__(self, name, number, link):
        self.game_name = name
        self.game_number = number
        self.game_link = link

    @property
    def serialize(self):
        return {'game_number': self.game_number,
                'game_name': self.game_name,
                'game_link': self.game_link}

    def __repr__(self):
        return "Game Number:" + str(self.game_number)


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    game_price = db.Column(db.Float)
    time = db.Column(db.TIMESTAMP, default=datetime.datetime.now())

    def __init__(self, price):
        self.game_price = price

    def __repr__(self):
        return "Game Id:" + str(self.game_id)


# def create_date():
#     game1 = Game("123", "2312", "123")
#     price1 = Price('11')
#     game1.game_price.append(price1)
#     db.session.add(game1)
#     db.session.commit()


# create_date()
db.create_all()
