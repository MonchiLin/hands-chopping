import api.view  as view
from config import Config
from app import create_app
from flask_script import Manager, Shell, Server

app = create_app()
app.debug = True
manager = Manager(app)


def make_shell_context():
    manager.add_command("shell", Shell(make_context=make_shell_context))
    return dict(app=app, db=Config.db)


api = Config.api
api.add_resource(view.GameList, '/games/')
api.add_resource(view.PriceList, '/prices/')

if __name__ == '__main__':
    manager.run()
