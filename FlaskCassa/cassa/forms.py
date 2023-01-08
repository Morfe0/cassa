from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Length, DataRequired, ValidationError
from cassa.model import User


class LoginForm(FlaskForm):
    matricola = StringField(label="MATRICOLA", validators=[DataRequired()])
    password = PasswordField(label="PASSWORD", validators=[DataRequired()])
    submit = SubmitField(label="ACCEDI")


class RegisterForm(FlaskForm):

    def validate_matricola(self, matricola_to_check):
        user = User.query.filter_by(matricola=matricola_to_check.data).first()
        if user:
            raise ValidationError('La matricola inserita è già registrata')

    matricola = StringField(label="MATRICOLA", validators=[Length(min=2, max=6), DataRequired()])
    password = PasswordField(label="PASSWORD", validators=[Length(min=6, max=6), DataRequired()])
    submit = SubmitField(label="REGISTRA")


class PurchaseForm(FlaskForm):
    barcode = StringField(label="barcode", validators=[Length(min=12, max=12), DataRequired()])
    submit = SubmitField(label='conferma')


class NewReceiptForm(FlaskForm):
    submit = SubmitField(label='nuovo scontrino')