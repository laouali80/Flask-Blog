from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime


app = Flask(__name__)



# to secure forms from across attacks, modifiying cokies
app.config['SECRET_KEY'] = 'c455d91a712ebbaa80f06ee0d2c9ae8d'

# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
# allows us to create the models
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    # post make a 1:M relationship btw the User and Post, backref is use to know the user of a post, lazy grabs all the posts of the user in sql
    posts = db.relationship('Post', backref='author', lazy=True) 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}'')"
    


posts = [
    {
        'author': 'Laouali Bachir',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2023'
    },

    {
        'author': 'Corey Shafer',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'September 21, 2023'
    }
]
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Account created for { form.username.data}!', category='success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)



@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', category='danger')
    return render_template('login.html', title='Log In', form=form)



if __name__ == '__main__':
    app.run(debug=True)