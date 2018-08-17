import api.view  as view
from config import Config

# class GameResource(Resource):
#     def get(self):
#         return model.Game.query.all()
#
#
# api.add_resource(GameResource, '/')


api = Config.api
api.add_resource(view.Game, '/')


if __name__ == '__main__':
    app = Config.app
    app.run(debug=True)
