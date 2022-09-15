import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import forms

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfgsfdgsdfgsdfgsdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bankera.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Saskaita(db.Model):
    __tablename__ = "saskaita"
    id = db.Column(db.Integer, primary_key=True)
    numeris = db.Column("Numeris", db.String)
    bankas = db.Column("Bankas", db.String)
    balansas = db.Column("Balansas", db.Integer)
    asmuo_id = db.Column(db.Integer, db.ForeignKey("asmuo.id"))
    bankas_id = db.Column(db.Integer, db.ForeignKey("bankas.id"))
    asmuo = db.relationship("Asmuo", back_populates="saskaitos")
    bankai = db.relationship("Bankas")

class Asmuo(db.Model):
    __tablename__ = "asmuo"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String)
    pavarde = db.Column("Pavardė", db.String)
    asmens_kodas = db.Column("Asmens kodas", db.Integer)
    tel_numeris = db.Column("Telefono numeris", db.String)
    saskaitos = db.relationship("Saskaita", back_populates="asmuo")

class Bankas(db.Model):
    __tablename__ = "bankas"
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column("Pavadinimas", db.String)
    adresas = db.Column("Adresas", db.String)
    banko_kodas = db.Column("Banko kodas", db.String)
    swift = db.Column("SWIFT kodas", db.String)
    saskaitos = db.relationship("Saskaita")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/saskaitos")
def accounts():
    try:
        visos_saskaitos = Saskaita.query.all()
    except:
        visos_saskaitos = []
    return render_template("saskaitos.html", visos_saskaitos=visos_saskaitos)


@app.route("/asmenys")
def persons():
    try:
        visi_asmenys = Asmuo.query.all()
    except:
        visi_asmenys = []
    return render_template("asmenys.html", visi_asmenys=visi_asmenys)



@app.route("/nauja_saskaita", methods=["GET", "POST"])
def new_account():
    db.create_all()
    forma = forms.SaskaitaForm()
    if forma.validate_on_submit():
        nauja_saskaita = Saskaita(numeris=forma.numeris.data, balansas=forma.balansas.data, asmuo_id=forma.asmuo.data.id)
        db.session.add(nauja_saskaita)
        db.session.commit()
        return redirect(url_for('accounts'))
    return render_template("prideti_saskaita.html", form=forma)


@app.route("/delete/<int:id>")
def delete(id):
    uzklausa = Saskaita.query.get(id)
    db.session.delete(uzklausa)
    db.session.commit()
    return redirect(url_for('accounts'))


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    form = forms.SaskaitaForm()
    saskaita = Saskaita.query.get(id)
    if form.validate_on_submit():
        saskaita.numeris = form.numeris.data
        saskaita.balansas = form.balansas.data
        saskaita.asmuo_id = form.asmuo.data.id
        db.session.commit()
        return redirect(url_for('accounts'))
    return render_template("update.html", form=form, saskaita=saskaita)

@app.route("/naujas_vaikas", methods=["GET", "POST"])
def new_person():
    db.create_all()
    forma = forms.AsmuoForm()
    if forma.validate_on_submit():
        naujas_asmuo = Asmuo(vardas=forma.vardas.data,
                               pavarde=forma.pavarde.data,
                             asmens_kodas = forma.asmens_kodas.data,
                             tel_numeris = forma.tel_numeris.data)
        db.session.add(naujas_asmuo)
        db.session.commit()
        return redirect(url_for('persons'))
    return render_template("prideti_asmeni.html", form=forma)

@app.route("/asmuo_delete/<int:id>")
def asmuo_delete(id):
    uzklausa = Asmuo.query.get(id)
    db.session.delete(uzklausa)
    db.session.commit()
    return redirect(url_for('persons'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
    db.create_all()