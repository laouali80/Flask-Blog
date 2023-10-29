from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post   
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.helpers import save_picture



@app.route('/')
@app.route('/home')
def home():
    # waiting a get request for the page we want to go to
    page = request.args.get('page', 1, type=int)
    
    # querying all the posts by pages
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['POST', 'GET'])
def register():
    # check if the user is already login to redirect him/her to home pagge always when refresh
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)



@app.route('/login', methods=['POST', 'GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()


        if user and bcrypt.check_password_hash(user.password, form.password.data):

            # acts as a session (login_user) and if remember is true then create cookies else don't create
            login_user(user, remember=form.remember.data)

            # allw us to go to the page that we want to access after login
            next_page = request.args.get('next')

            flash(f'You have been logged in!', category='success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', category='danger')
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/account', methods=['GET', 'POST'])
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

        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file )
    
    return render_template('account.html', title='Account', 
                           image_file=image_file, form=form)



@app.route('/post/new',methods=['GET', 'POST'] )
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        #author will give us access to the whole user object
        post = Post(title=form.title.data, content=form.content.data, author=current_user)

        db.session.add(post)
        db.session.commit()

        flash('Your pos has been created!', category='success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')



@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # checking if the post belong to the user to allow him/her update
    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        
        db.session.commit()

        flash('Your post has been updated!', 'success')

        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    
    return render_template('create_post.html', title='Update Post', 
                           form=form, legend='Update Post')


@app.route('/post/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # checking if the post belong to the user to allow him/her update
    if post.author != current_user:
        abort(403)

    db.session.delete(post)    
    db.session.commit()

    flash('Your post has been deleted!', 'success')

    return redirect(url_for('home'))
    

    


@app.route("/user/<string:username>")
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