import secrets
import os
from flaskblog import app, mail
from flask_mail import Message
from PIL import Image
from flask import url_for

def save_picture(form_picture):
    """ the function allows us to save a picture upload in our static/profile_pics"""

    random_hex = secrets.token_hex(8)

    # to get the extension of a file
    # _ means we don't need the data store in _ == f_name
    _, f_ext = os.path.splitext(form_picture.filename)

    # assigning a new name with hex num to our picture
    picture_fn = random_hex + f_ext

    # storing the picture in profile_pics folder
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resize the picture
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Rest Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f''''To rreset your password, visit the following link:
    {url_for('reset_token', token=token,  _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.'''

    mail.send(msg)