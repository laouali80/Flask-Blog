from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config




db = SQLAlchemy()

# to generate harsh password
bcrypt = Bcrypt()

#initializaton or config of the login 
login_manager = LoginManager()

# setting the login page (when a user try to acces a page without being login)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'



mail = Mail()



# it allows us to create #tes instances with #tes configurations
def create_app(config_class=Config):
    app = Flask(__name__)

    ## passing the configurations
    app.config.from_object(Config)


    # To initialize
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    
    # allows us to create the models
    app.app_context().push()
    

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
