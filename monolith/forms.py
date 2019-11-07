import wtforms as f
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired()])
    password = f.PasswordField('password', validators=[DataRequired()])
    display = ['email', 'password']


class UserForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired()])
    firstname = f.StringField('firstname', validators=[DataRequired()])
    lastname = f.StringField('lastname', validators=[DataRequired()])
    password = f.PasswordField('password', validators=[DataRequired()])
    dateofbirth = f.DateField('dateofbirth', format='%d/%m/%Y')
    display = ['email', 'firstname', 'lastname', 'password', 'dateofbirth']


class StoryForm(FlaskForm):
    text = f.TextAreaField('text', validators=[Length(max=1000, message=(u'Your story is too long!')), DataRequired()])
    display = ['text']


class SelectDiceSetForm(FlaskForm):
    dicenumber = f.IntegerField(id="dicenumber", label="Insert dice number: ", default=0)
    dicesetid = f.SelectField(id="dicesetid", label="Select dice set: ", choices=[('basic', 'Basic set'), ('halloween', 'Halloween set')], default='basic')
    display = ['dicenumber', 'dicesetid']


class StoryFilter(FlaskForm):
    init_date = f.DateField('init_date')
    end_date = f.DateField('end_date')
    display = ['init_date', 'end_date']

    def validate_on_submit(self):
        result = super(StoryFilter, self).validate()
        try:
            result = result and (self.init_date.data <= self.end_date.data)
        except TypeError:
            result = False
        return result

