import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

# to secure forms from across attacks, modifiying cokies
app.config['SECRET_KEY'] = 'c455d91a712ebbaa80f06ee0d2c9ae8d'

# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
# allows us to create the models
app.app_context().push()

# to generate harsh password
bcrypt = Bcrypt(app)

#initializaton or config of the login 
login_manager = LoginManager(app)

# setting the login page (when a user try to acces a page without being login)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# configure the email sent
app.config['MAIL_SERVER'] = 'smtp.googlemail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER') 
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS') 
mail = Mail(app)


from flaskblog import routes
