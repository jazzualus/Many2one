from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
import app

def asmuo_query():
    return app.Asmuo.query

class SaskaitaForm(FlaskForm):
    numeris = StringField('Numeris', [DataRequired()])
    balansas = StringField('Balansas', [DataRequired()])
    asmuo = QuerySelectField(query_factory=asmuo_query, allow_blank=True, get_label="vardas")
    bankas = StringField('Bankas', [DataRequired()])
    submit = SubmitField('Įvesti')


class AsmuoForm(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    pavarde = StringField('Pavardė', [DataRequired()])
    asmens_kodas = StringField('Asmens kodas', [DataRequired()])
    tel_numeris = StringField('Telefono numeris', [DataRequired()])
    submit = SubmitField('Įvesti')