from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .model import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)                           # integrate database into app
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'    # ???
    login_manager.init_app(app)                # integrate login_manaher into app
    
    @login_manager.user_loader                 # necessary element
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)     # integrate blueprint into app
    
    return app
    
#set FLASK_APP=platform && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
