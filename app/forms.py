from wtforms import Form, BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email ', [validators.Length(min=6, max=50)])
    name = TextField('Name', [validators.Length(min=3, max=20)])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match!')
    ])
    confirm = PasswordField('Confirm password')
    accept_tos = BooleanField('I am to blame myself only', [validators.Required()])
