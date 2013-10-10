from flask.ext.wtf import Form
from wtforms import FileField
from wtforms.validators import Required

class SendForm(Form):
    file = FileField('file', validators = [Required()])