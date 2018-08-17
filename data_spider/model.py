import datetime

from config import Config

db = Config.db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.String, unique=True)
    game_name = db.Column(db.String)
    gama_price = db.relationship('Price', backref='game', lazy='dynamic')
    gama_link = db.Column(db.String)

    def __init__(self, name, number, link):
        self.game_name = name
        self.game_number = number
        self.gama_link = link


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    gama_price = db.Column(db.Float)
    time = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    def __init__(self, price):
        self.gama_price = price

# def create_date():
#     game1 = Game("123", "2312", "123")
#     price1 = Price('11')
#     game1.gama_price.append(price1)
#     db.session.add(game1)
#     db.session.commit()


# create_date()
# db.create_all()