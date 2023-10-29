from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user
#allow to upload file 
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # flaskforms looks for any func starting by validate_ and it will look if we have any field of name username
    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            # this will be thrown as a form validation error
            raise ValidationError('Existing username. Please choose a different username.')


    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            # this will be thrown as a form validation error
            raise ValidationError('Existing email. Please choose a different email.')
    
class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # flaskforms looks for any func starting by validate_ and it will look if we have any field of name username
    def validate_username(self, username):

        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()

            if user:
                # this will be thrown as a form validation error
                raise ValidationError('Existing username. Please choose a different username.')


    def validate_email(self, email):

        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                # this will be thrown as a form validation error
                raise ValidationError('Existing email. Please choose a different email.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user is None:
            # this will be thrown as a form validation error
            raise ValidationError('There is no account with that email. You must register first.')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
