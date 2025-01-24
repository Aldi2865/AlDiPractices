
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired

class AmmunitionForm(FlaskForm):
    type = StringField('Type', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    storage_location = StringField('Storage Location', validators=[DataRequired()])
    expiration_date = DateField('Expiration Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')