from config import Config

db = Config.db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.String, unique=True)
    game_name = db.Column(db.String)
    game_price = db.relationship('Price', backref='game', lazy='dynamic')
    game_link = db.Column(db.String)
    game_tag = db.Column(db.String, default=None)
    game_Genre = db.Column(db.String, default=None)
    game_picture = db.Column(db.String)
    game_preview = db.Column(db.String, default=None)
    game_detail = db.Column(db.String, default='')
    game_jianpin = db.Column(db.String, default='')
    game_quanpin = db.Column(db.String, default='')

    def __init__(self, name, number, link, picture, detail):
        self.game_name = name
        self.game_number = number
        self.game_link = link
        self.game_picture = picture
        self.game_detail = detail

    @property
    def serialize(self):
        return {
            'id': self.id,
            'game_number': self.game_number,
            'game_name': self.game_name,
            'game_link': self.game_link,
            'game_tag': self.game_tag,
            'game_Genre': self.game_Genre,
            'game_picture': self.game_picture,
            'game_preview': self.game_preview,
            'game_detail': self.game_detail
        }

    def __repr__(self):
        return "Game Number:" + self.game_number


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    game_price = db.Column(db.Float)
    time = db.Column(db.TIMESTAMP, server_default=db.func.now())

    def __init__(self, price):
        self.game_price = price

    @property
    def serialize(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'game_price': self.game_price,
            'time': self.time
        }

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
