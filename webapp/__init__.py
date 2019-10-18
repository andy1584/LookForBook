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

    # blueprint for auth routes in our flask_app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)     # integrate blueprint into app

    return app
    #> set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run

app = create_app()

# testing Celery  # # # # # # # # # # # # # # # # # # # # # # #
                                                              #
@app.route('/celery')                                         #
def run_task():                                               #
    from .tasks import worker_task                            #
    result = worker_task.delay()                              #
    print(result.state)                                       #
    print("\n*** Далее - get() ***\n")                        #
    print(result.get())                                       #
    return "Функция проверки Celery"                          #
                                                              #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #