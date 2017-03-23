from wtforms import Form, BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email ', [validators.Length(min=6, max=50), validators.Email(message='Enter correct email')])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match!')
    ])
    confirm = PasswordField('Confirm password')
    fname = TextField('Firstname', [validators.Length(min=3, max=20)])
    lname = TextField('Lastname', [validators.Length(min=3, max=20)])
    phone = TextField('Phone Number', [validators.Length(min=7, max=17)])
    university = TextField('University', [validators.Length(min=0, max=20)])
    paycheck = TextField('Paycheck', [validators.Length(min=0, max=20)])    
    #accept_tos = BooleanField('I am to blame myself only', [validators.Required()])
