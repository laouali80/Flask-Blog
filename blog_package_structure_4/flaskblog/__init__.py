from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

# to secure forms from across attacks, modifiying cokies
app.config['SECRET_KEY'] = 'c455d91a712ebbaa80f06ee0d2c9ae8d'

# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
# allows us to create the models
app.app_context().push()

from flaskblog import routes
