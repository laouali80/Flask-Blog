from flask import Blueprint, render_template, url_for, flash, redirect, request
from flaskblog import db, bcrypt
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                             RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post   
from flask_login import login_user, current_user, logout_user, login_required
from .helpers import save_picture, send_reset_email


users = Blueprint('users', __name__)



@users.route('/register', methods=['POST', 'GET'])
def register():
    # check if the user is already login to redirect him/her to home pagge always when refresh
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # flaskForm handle the verification of dupplicate username or email with the validate_username and validate_email function in the forms.py
        new_user = User(username=username, email=email, password=hash_password)
        
        db.session.add(new_user)
        db.session.commit()

        flash(f'Account created for { username.title() }!', category='success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['POST', 'GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()

    
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()


        if user and bcrypt.check_password_hash(user.password, form.password.data):

            # acts as a session (login_user) and if remember is true then create cookies else don't create
            login_user(user, remember=form.remember.data)

            # allw us to go to the page that we want to access after login
            next_page = request.args.get('next')

            flash(f'You have been logged in!', category='success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', category='danger')
    return render_template('login.html', title='Log In', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():
        # checking if the user has change his/her profile image
        if form.picture.data:
            picture_file =save_picture(form.picture.data)
            # updating the user profile pic
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash('Your account has been updated!', category='success')

        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file )
    
    return render_template('account.html', title='Account', 
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    # waiting a get request for the page we want to go to
    page = request.args.get('page', 1, type=int)
    
    # getting the user request of the user post wanted
    user = User.query.filter_by(username=username).first_or_404()

    # querying all the posts of the user wanted by pages
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['POST', 'GET'])
def reset_request():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to rest your password.', category='info')

        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expired token', category='warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()

    if form.validate_on_submit():
        password = form.password.data

        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user.password = hash_password
        db.session.commit()

        flash(f'Yor password has been upddated! You are now able to log in', category='success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Reset Password', form=form)

 