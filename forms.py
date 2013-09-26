from flask.ext.wtf import Form
from wtforms import FileField, PasswordField
from wtforms.validators import ValidationError, Required, Length

def password_check(form, field):
    if len(field.data) > 100:
        raise ValidationError('Field must be less than 100 characters')
    badchars = set('\"\\*^%;|><?')
    if any((c in badchars) for c in field.data):
        raise ValidationError('Bad symbols in field')

class SendForm(Form):
    file = FileField('file', validators = [Required()])
    img = FileField('img', validators = [Required()])
    pwd = PasswordField('pwd', validators = [Length(max = 100, message = "Max password length - 100"), password_check])