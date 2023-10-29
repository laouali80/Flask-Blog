// setting an enviroment viarable for the app running , Linux set = export
// allow the use of flask run 
set FLASK_APP=flaskblog.py

// setting the running unstop
set FLASK_DEBUG=1

// if we want to run the file with python (inside flaskblog.py) e.g python3 flaskblog.py
if __name__=='__main__':
    app.run(debug=True)

ctrl + shift + r : strong refresh

pip3 install flask-wtf

to generate an app secret key
python3
import secrets
secrets.token_hex(16)


pip3 install flask_sqlalchemy

from flaskblog import db
db.create_all()

// query all the data in user table (select *)
User.query.all()

// query the first data in the table
User.query.first()

//query with constrainte
User.query.filter_by(username='l').all()
User.query.filter_by(username='l').first()

//query by id
us = User.query.get(1)

// backref usage
post = Post.query.first()
post.author =>> User('lbid', 'lbid@gmail.com', '21345678')

// dropping all the table with python
db.drop_all()


//hashing password
pip3 install flask-bcrypt


//for the login authentification
pip3 install flask-login

// helps to resize a picture
pip3 install Pillow

// query by page (having each page with 5 posts)
posts= Post.query.paginate(per_page=5)

// to access the other pages by a get request
localhost:5000/home?page=3

