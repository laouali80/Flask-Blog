from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)


# to secure forms from across attacks, modifiying cokies
app.config['SECRET_KEY'] = 'c455d91a712ebbaa80f06ee0d2c9ae8d'

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