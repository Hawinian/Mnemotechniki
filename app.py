from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import datetime
from passlib.hash import sha256_crypt

from sqlalchemy.sql.functions import now

from forms import cwiczenie1Form, cwiczenie2Form, cwiczenie3Form, cwiczenie4Form, cwiczenie5Form, cwiczenie6Form, cwiczenie7Form, cwiczenie8Form, loginForm, registerForm
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LICENCJATEPI'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



class MyDateTime(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M')
        return value

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    login = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))
    role = db.Column(db.String(10))

    def __init__(self, name, login, password, role='user'):
        self.name = name
        self.login = login
        self.password = password
        self.role = role

class results(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


    def __init__(self, user_id, exercise_id, score, date):
        self.user_id = user_id
        self.exercise_id = exercise_id
        self.score = score
        self.date = date




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = loginForm()
    if form.validate_on_submit():
        dane = request.form.to_dict()
        username = users.query.filter_by(login=dane["login"]).first()
        if username:
            if sha256_crypt.verify(dane["password"], username.password):
                session['id'] = username._id
                session['name'] = username.name
                session['login'] = username.login
                session['logged'] = True
                session['role'] = username.role
                return redirect(url_for("index"))
            else:
                return render_template('login.html', form=form, Passerror='Hasło nie pasuje')
        else:
            return render_template('login.html', form=form, Loginerror='Taki użytkownik nie istnieje')
    return render_template('login.html', form=form)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = registerForm()
    if form.validate_on_submit():
        dane = request.form.to_dict()
        username = users.query.filter_by(login=dane["login"]).first()
        if username:
            return render_template('register.html', form=form, Validerror='Taki użytkownik już istnieje!')

        hash = sha256_crypt.hash(dane["password"])
        new_user = users(dane["name"], dane["login"], hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop("id", None)
    session.pop("name", None)
    session.pop("login", None)
    session.pop("logged",None)
    session.pop("role", None)
    return render_template('index.html')

@app.route('/user')
def user():
    u = users(name='john', login='johnny', password="haha")
    db.session.add(u)
    db.session.commit()
    return redirect(url_for("view"))

@app.route('/view')
def view():
    if session.get('logged') == True:
        if session['role'] == 'admin':
            return render_template("view.html", valuesu = users.query.all(), valuesw = results.query.all(),)
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")

@app.route('/konto')
def konto():
    return render_template("konto.html", twyniki = results.query.filter_by(user_id=session["id"]).all())

@app.route('/loci')
def loci():
    return render_template('loci.html')

@app.route('/glowna')
def glowna():
    return render_template('index.html')

@app.route('/pamiec')
def pamiec():
    return render_template('pamiec.html')

@app.route('/mnemotechniki')
def mnemotechniki():
    return render_template('mnemotechniki.html')

@app.route('/skojarzenia')
def skojarzenia():
    return render_template('skojarzenia.html')

@app.route('/grey')
def grey():
    return render_template('grey.html')

@app.route('/akronimy')
def akronimy():
    return render_template('akronimy.html')

@app.route('/liczby')
def liczby():
    return render_template('liczby-ksztalty.html')

@app.route('/podzial_pamieci')
def podzial_pamieci():
    return render_template('podzial_pamieci.html')

@app.route('/rodzaje_pamieci')
def rodzaje_pamieci():
    return render_template('rodzaje-pamieci.html')

@app.route('/polepszenie_pamieci')
def polepszenie_pamieci():
    return render_template('polepszenie-pamieci.html')

@app.route('/zawodnosc-pamieci')
def zawodnosc_pamieci():
    return render_template('zawodnosc-pamieci.html')

@app.route('/czynnosci_pamieciowe')
def czynnosci_pamieciowe():
    return render_template('czynnosci-pamieciowe.html')\

@app.route('/pamiec_przemijajaca')
def pamiec_przemijajaca():
    return render_template('pamiec_przemijajaca.html')\

@app.route('/pamiec_trwala')
def pamiec_trwala():
    return render_template('pamiec_trwala.html')

@app.route('/polkule')
def polkule():
    return render_template('polkule.html')

@app.route('/mapy')
def mapy():
    return render_template('mapy.html')

@app.route('/slowka')
def slowka():
    return render_template('slowka.html')

@app.route('/serwis')
def serwis():
    return render_template('serwis.html')

@app.route('/cwiczenie1')
def cwiczenie1():
    return render_template('cwiczenie1.html')

@app.route('/cwiczenie1start')
def cwiczenie1start():
    return render_template('cwiczenie1start.html')

@app.route('/cwiczenie1formularz', methods=["GET", "POST"])
def cwiczenie1formularz():
    form = cwiczenie1Form()
    if form.is_submitted():
        rezultat = ''
        wynik = 0
        result = request.form
        dane = {'jeden': 'Brak odpowiedzi', 'dwa': 'Brak odpowiedzi', 'trzy': 'Brak odpowiedzi', 'cztery': 'Brak odpowiedzi', 'piec': 'Brak odpowiedzi', 'szesc': 'Brak odpowiedzi', 'siedem': 'Brak odpowiedzi', 'osiem': 'Brak odpowiedzi', 'dziewiec': 'Brak odpowiedzi','dziesiec': 'Brak odpowiedzi'}
        dane = request.form.to_dict()
        Odpowiedzi = {'1': 'false', '2': 'false', '3': 'false', '4': 'false', '5': 'false', '6': 'false', '7': 'false', '8': 'false', '9': 'false', '10': 'false'}
        if dane['jeden'] == 'ogród':
            wynik += 1
            Odpowiedzi['1'] = 'true'
        if dane['dwa'] == 'myśliwiec':
            wynik += 1
            Odpowiedzi['2'] = 'true'
        if dane['trzy'] == 'kotek':
            wynik += 1
            Odpowiedzi['3'] = 'true'
        if dane['cztery'] == 'książka':
            wynik += 1
            Odpowiedzi['4'] = 'true'
        if dane['piec'] == 'kuzyn':
            wynik += 1
            Odpowiedzi['5'] = 'true'
        if dane['szesc'] == 'filozof':
            wynik += 1
            Odpowiedzi['6'] = 'true'
        if dane['siedem'] == 'klapek':
            wynik += 1
            Odpowiedzi['7'] = 'true'
        if dane['osiem'] == 'pływanie':
            wynik += 1
            Odpowiedzi['8'] = 'true'
        if dane['dziewiec'] == 'film krótkometrażowy':
            wynik += 1
            Odpowiedzi['9'] = 'true'
        if dane['dziesiec'] == 'komputer':
            wynik += 1
            Odpowiedzi['10'] = 'true'

        if wynik < 4:
            rezultat = 'bad'
        if 4 <= wynik <= 7:
            rezultat = 'medium'
        if wynik > 7:
            rezultat = 'good'


        if session.get('logged') == True:
            now = datetime.now()
            new_result = results(session['id'], 1, wynik, now)
            db.session.add(new_result)
            db.session.commit()

        return render_template('cwiczenie1wynik.html', test=result, wynik=wynik, odpowiedzi=Odpowiedzi, dane=dane, rezultat=rezultat)
    return render_template('cwiczenie1formularz.html', form=form)

@app.route('/cwiczenie2')
def cwiczenie2():
    return render_template('cwiczenie2.html')

@app.route('/cwiczenie2start')
def cwiczenie2start():
    return render_template('cwiczenie2start.html')

@app.route('/cwiczenie2formularz', methods=["GET", "POST"])
def cwiczenie2formularz():
    form = cwiczenie2Form()
    if form.is_submitted():
        rezlutat = ''
        wynik = 0
        result = request.form
        dane = {'jeden': 'Brak odpowiedzi', 'dwa': 'Brak odpowiedzi', 'trzy': 'Brak odpowiedzi', 'cztery': 'Brak odpowiedzi', 'piec': 'Brak odpowiedzi', 'szesc': 'Brak odpowiedzi', 'siedem': 'Brak odpowiedzi', 'osiem': 'Brak odpowiedzi', 'dziewiec': 'Brak odpowiedzi'}
        dane = request.form.to_dict()
        Odpowiedzi = {'1': 'false', '2': 'false', '3': 'false', '4': 'false', '5': 'false', '6': 'false', '7': 'false', '8': 'false', '9': 'false'}
        if dane['jeden'] == 'pchła':
            wynik += 1
            Odpowiedzi['1'] = 'true'
        if dane['dwa'] == 'papieros' or dane['dwa'] == 'papierosy':
            wynik += 1
            Odpowiedzi['2'] = 'true'
        if dane['trzy'] == 'okulary' or dane['trzy'] == 'okular':
            wynik += 1
            Odpowiedzi['3'] = 'true'
        if dane['cztery'] == 'jedzenie':
            wynik += 1
            Odpowiedzi['4'] = 'true'
        if dane['piec'] == 'młyn':
            wynik += 1
            Odpowiedzi['5'] = 'true'
        if dane['szesc'] == 'maszt':
            wynik += 1
            Odpowiedzi['6'] = 'true'
        if dane['siedem'] == 'lodówka':
            wynik += 1
            Odpowiedzi['7'] = 'true'
        if dane['osiem'] == 'ksiądz':
            wynik += 1
            Odpowiedzi['8'] = 'true'
        if dane['dziewiec'] == 'gazeta':
            wynik += 1
            Odpowiedzi['9'] = 'true'

        if wynik < 4:
            rezultat = 'bad'
        if 4 <= wynik <= 7:
            rezultat = 'medium'
        if wynik > 7:
            rezultat = 'good'

        if session.get('logged') == True:
            now = datetime.now()
            new_result = results(session['id'], 2, wynik, now)
            db.session.add(new_result)
            db.session.commit()

        return render_template('cwiczenie2wynik.html', test=result, wynik=wynik, odpowiedzi=Odpowiedzi, dane=dane, rezultat=rezultat)
    return render_template('cwiczenie2formularz.html', form=form)

@app.route('/cwiczenie3')
def cwiczenie3():
    return render_template('cwiczenie3.html')

@app.route('/cwiczenie3start')
def cwiczenie3start():
    return render_template('cwiczenie3start.html')

@app.route('/cwiczenie3formularz', methods=["GET", "POST"])
def cwiczenie3formularz():
    form = cwiczenie3Form()
    if form.is_submitted():
        rezultat =''
        wynik = 0
        result = request.form
        dane = {'jeden': 'Brak odpowiedzi', 'dwa': 'Brak odpowiedzi', 'trzy': 'Brak odpowiedzi', 'cztery': 'Brak odpowiedzi', 'piec': 'Brak odpowiedzi', 'szesc': 'Brak odpowiedzi', 'siedem': 'Brak odpowiedzi', 'osiem': 'Brak odpowiedzi', 'dziewiec': 'Brak odpowiedzi', 'dziesiec': 'Brak odpowiedzi'}
        dane = request.form.to_dict()
        rozwiazania = request.form.to_dict()
        Odpowiedzi = {'jeden': 'false', 'dwa': 'false', 'trzy': 'false', 'cztery': 'false', 'piec': 'false', 'szesc': 'false', 'siedem': 'false', 'osiem': 'false', 'dziewiec': 'false', 'dziesiec': 'false'}


        if 'Hiszpania' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Hiszpania']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Hiszpania'}

        if 'Bahamy' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Bahamy']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Bahamy'}

        if 'Irak' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Irak']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Irak'}

        if 'Ghana' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Ghana']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Ghana'}

        if 'Jordania' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Jordania']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Jordania'}

        if 'Białoruś' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Białoruś']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Białoruś'}

        if 'Indie' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Indie']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Indie'}

        if 'Boliwia' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Boliwia']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Boliwia'}

        if 'Arabia Saudyjska' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Arabia Saudyjska']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Arabia Saudyjska'}

        if 'Pakistan' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Pakistan']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Pakistan'}

        if wynik < 4:
            rezultat = 'bad'
        if 4 <= wynik <= 7:
            rezultat = 'medium'
        if wynik > 7:
            rezultat = 'good'

        if session.get('logged') == True:
            now = datetime.now()
            new_result = results(session['id'], 3, wynik, now)
            db.session.add(new_result)
            db.session.commit()


        return render_template('cwiczenie3wynik.html', test=result, wynik=wynik, odpowiedzi=Odpowiedzi, dane=dane, rezultat=rezultat)
    return render_template('cwiczenie3formularz.html', form=form)

@app.route('/cwiczenie4')
def cwiczenie4():
    return render_template('cwiczenie4.html')

@app.route('/cwiczenie4start')
def cwiczenie4start():
    return render_template('cwiczenie4start.html')

@app.route('/cwiczenie4formularz', methods=["GET", "POST"])
def cwiczenie4formularz():
    form = cwiczenie4Form()
    if form.is_submitted():
        rezultat = ''
        wynik = 0
        result = request.form
        dane = {'jeden': 'Brak odpowiedzi', 'dwa': 'Brak odpowiedzi', 'trzy': 'Brak odpowiedzi', 'cztery': 'Brak odpowiedzi', 'piec': 'Brak odpowiedzi', 'szesc': 'Brak odpowiedzi', 'siedem': 'Brak odpowiedzi', 'osiem': 'Brak odpowiedzi', 'dziewiec': 'Brak odpowiedzi', 'dziesiec': 'Brak odpowiedzi'}
        dane = request.form.to_dict()
        rozwiazania = request.form.to_dict()
        Odpowiedzi = {'jeden': 'false', 'dwa': 'false', 'trzy': 'false', 'cztery': 'false', 'piec': 'false', 'szesc': 'false', 'siedem': 'false', 'osiem': 'false', 'dziewiec': 'false', 'dziesiec': 'false'}


        if 'Grecja' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Grecja']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Grecja'}

        if 'Jemen' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Jemen']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Jemen'}

        if 'Norwegia' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Norwegia']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Norwegia'}

        if 'Bułgaria' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Bułgaria']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Bułgaria'}

        if 'Łotwa' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Łotwa']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Łotwa'}

        if 'Czechy' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Czechy']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Czechy'}

        if 'Madagaskar' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Madagaskar']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Madagaskar'}

        if 'Austria' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Austria']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Austria'}

        if 'Czarnogóra' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Czarnogóra']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Czarnogóra'}

        if 'Kanada' in rozwiazania.values():
            wynik += 1
            listOfKeys = [key for (key, value) in rozwiazania.items() if value == 'Kanada']
            Odpowiedzi[listOfKeys[0]] = 'true'
            rozwiazania = {key: val for key, val in rozwiazania.items() if val != 'Kanada'}

        if wynik < 4:
            rezultat = 'bad'
        if 4 <= wynik <= 7:
            rezultat = 'medium'
        if wynik > 7:
            rezultat = 'good'


        if session.get('logged') == True:
            now = datetime.now()
            new_result = results(session['id'], 4, wynik, now)
            db.session.add(new_result)
            db.session.commit()

        return render_template('cwiczenie4wynik.html', test=result, wynik=wynik, odpowiedzi=Odpowiedzi, dane=dane, rezultat=rezultat)
    return render_template('cwiczenie4formularz.html', form=form)

@app.route('/cwiczenie5')
def cwiczenie5():
    return render_template('cwiczenie5.html')

@app.route('/cwiczenie5start')
def cwiczenie5start():
    return render_template('cwiczenie5start.html')

@app.route('/cwiczenie5formularz', methods=["GET", "POST"])
def cwiczenie5formularz():
    form = cwiczenie5Form()
    if form.is_submitted():
        rezultat = ''
        wynik = 0
        result = request.form
        dane = {'pociag': 'Brak odpowiedzi', 'drabina': 'Brak odpowiedzi' }
        dane = request.form.to_dict()
        Odpowiedzi = {'1': 'false', '2': 'false', '3': 'false', '4': 'false', '5': 'false', '6': 'false', '7': 'false', '8': 'false', '9': 'false', '10': 'false'}
        Odp = {'1': 'false', '2': 'false', '3': 'false', '4': 'false', '5': 'false', '6': 'false', '7': 'false', '8': 'false', '9': 'false', '10': 'false'}
        if dane['grupa1'] == 'bag':
            wynik += 1
            Odpowiedzi['1'] = dane['grupa1']
            Odp['1'] = 'true'
        else:
            Odpowiedzi['1'] = dane['grupa1']

        if dane['grupa2'] == 'armchair':
            wynik += 1
            Odpowiedzi['2'] = dane['grupa2']
            Odp['2'] = 'true'
        else:
            Odpowiedzi['2'] = dane['grupa2']

        if dane['grupa3'] == 'baby':
            wynik += 1
            Odpowiedzi['3'] = dane['grupa3']
            Odp['3'] = 'true'
        else:
            Odpowiedzi['3'] = dane['grupa3']

        if dane['grupa4'] == 'hospital':
            wynik += 1
            Odpowiedzi['4'] = dane['grupa4']
            Odp['4'] = 'true'
        else:
            Odpowiedzi['4'] = dane['grupa4']

        if dane['grupa5'] == 'chimney':
            wynik += 1
            Odpowiedzi['5'] = dane['grupa5']
            Odp['5'] = 'true'
        else:
            Odpowiedzi['5'] = dane['grupa5']

        if dane['grupa6'] == 'elderly':
            wynik += 1
            Odpowiedzi['6'] = dane['grupa6']
            Odp['6'] = 'true'
        else:
            Odpowiedzi['6'] = dane['grupa6']

        if dane['grupa7'] == 'clock':
            wynik += 1
            Odpowiedzi['7'] = dane['grupa7']
            Odp['7'] = 'true'
        else:
            Odpowiedzi['7'] = dane['grupa7']

        if dane['grupa8'] == 'kiosk':
            wynik += 1
            Odpowiedzi['8'] = dane['grupa8']
            Odp['8'] = 'true'
        else:
            Odpowiedzi['8'] = dane['grupa8']

        if dane['grupa9'] == 'donut':
            wynik += 1
            Odpowiedzi['9'] = dane['grupa9']
            Odp['9'] = 'true'
        else:
            Odpowiedzi['9'] = dane['grupa9']

        if dane['grupa10'] == 'microphone':
            wynik += 1
            Odpowiedzi['10'] = dane['grupa10']
            Odp['10'] = 'true'
        else:
            Odpowiedzi['10'] = dane['grupa10']

        if wynik < 4:
            rezultat = 'bad'
        if 4 <= wynik <= 7:
            rezultat = 'medium'
        if wynik > 7:
            rezultat = 'good'


        if session.get('logged') == True:
            now = datetime.now()
            new_result = results(session['id'], 5, wynik, now)
            db.session.add(new_result)
            db.session.commit()

        return render_template('cwiczenie5wynik.html', test=result, wynik=wynik, odpowiedzi=Odpowiedzi, odp=Odp, dane=dane, rezultat=rezultat)
    return render_template('cwiczenie5formularz.html', form=form)

@app.route('/cwiczenie6')
def cwiczenie6():
    return render_template('cwiczenie6.html')

@app.route('/cwiczenie6start')
def cwiczenie6start():
    return render_template('cwiczenie6start.html')

@app.route('/cwiczenie6formularz', methods=["GET", "POST"])
def cwiczenie6formularz():
    form = cwiczenie6Form()
    if form.is_submitted():
        rezultat = ''
        wynik = 0
        result = request.form
        dane = {'jeden': 'Brak odpowiedzi', 'dwa': 'Brak odpowiedzi', 'trzy': 'Brak odpowiedzi', 'cztery': 'Brak odpowiedzi', 'piec': 'Brak odpowiedzi', 'szesc': 'Brak odpowiedzi', 'siedem': 'Brak odpowiedzi', 'osiem': 'Brak odpowiedzi', 'dziewiec': 'Brak odpowiedzi'}
        dane = request.form.to_dict()
        Odpowiedzi = {'1': 'false', '2': 'false', '3': 'false', '4': 'false', '5': 'false', '6': 'false', '7': 'false', '8': 'false', '9': 'false', '10': 'false', '11': 'false', '12': 'false', '13': 'false', '14': 'false', '15': 'false'}
        if dane['jeden'] == 'czarownica':
            wynik += 1
            Odpowiedzi['1'] = 'true'
        if dane['dwa'] == 'parafia':
            wynik += 1
            Odpowiedzi['2'] = 'true'
        if dane['trzy'] == 'księgowy':
            wynik += 1
            Odpowiedzi['3'] = 'true'
        if dane['cztery'] == 'wiadomość':
            wynik += 1
            Odpowiedzi['4'] = 'true'
        if dane['piec'] == 'Śpiąca Królewna':
            wynik += 1
            Odpowiedzi['5'] = 'true'
        if dane['szesc'] == 'plaster':
            wynik += 1
            Odpowiedzi['6'] = 'true'
        if dane['siedem'] == 'deskorolka':
            wynik += 1
            Odpowiedzi['7'] = 'true'
        if dane['osiem'] == 'krytyk':
            wynik += 1
            Odpowiedzi['8'] = 'true'
        if dane['dziewiec'] == 'plac zabaw':
            wynik += 1
            Odpowiedzi['9'] = 'true'
        if dane['dziesiec'] == 'piosenka':
            wynik += 1
            Odpowiedzi['10'] = 'true'
        if dane['jedenascie'] == 'zdrajca':
            wynik += 1
            Odpowiedzi['11'] = 'true'
        if dane['dwanascie'] == 'matematyka':
            wynik += 1
            Odpowiedzi['12'] = 'true'
        if dane['trzynascie'] == 'Bielsko-Biała':
            wynik += 1
            Odpowiedzi['13'] = 'true'
        if dane['czternascie'] == 'stypendium':
            wynik += 1
            Odpowiedzi['14'] = 'true'
        if dane['pietnascie'] == 'gra komputerowa':
            wynik += 1
            Odpowiedzi['15'] = 'true'

        if wynik < 5:
            rezultat = 'bad'
        if 5 <= wynik <= 8:
            rezultat = 'medium'
        if 9 <= wynik <= 12:
            rezultat = 'good'
        if  wynik > 12:
            rezultat = 'very-good'

        if session.get('logged') == True:
            now = datetime.now()
            new_result = results(session['id'], 6, wynik, now)
            db.session.add(new_result)
            db.session.commit()

        return render_template('cwiczenie6wynik.html', test=result, wynik=wynik, odpowiedzi=Odpowiedzi, dane=dane, rezultat=rezultat)
    return render_template('cwiczenie6formularz.html', form=form)

@app.route('/cwiczenie7')
def cwiczenie7():
    return render_template('cwiczenie7.html')

@app.route('/cwiczenie7start')
def cwiczenie7start():
    return render_template('cwiczenie7start.html')

@app.route('/cwiczenie7formularz', methods=["GET", "POST"])
def cwiczenie7formularz():
    form = cwiczenie7Form()
    if form.is_submitted():
        rezultat= ''
        wynik = 0
        result = request.form
        dane = {'jeden': 'Brak odpowiedzi', 'dwa': 'Brak odpowiedzi', 'trzy': 'Brak odpowiedzi', 'cztery': 'Brak odpowiedzi', 'piec': 'Brak odpowiedzi', 'szesc': 'Brak odpowiedzi', 'siedem': 'Brak odpowiedzi', 'osiem': 'Brak odpowiedzi', 'dziewiec': 'Brak odpowiedzi'}
        dane = request.form.to_dict()
        Odpowiedzi = {'1': 'false', '2': 'false', '3': 'false', '4': 'false', '5': 'false', '6': 'false', '7': 'false', '8': 'false', '9': 'false', '10': 'false', '11': 'false', '12': 'false', '13': 'false', '14': 'false', '15': 'false'}
        if dane['jeden'] == 'żebro':
            wynik += 1
            Odpowiedzi['1'] = 'true'
        if dane['dwa'] == 'architekt':
            wynik += 1
            Odpowiedzi['2'] = 'true'
        if dane['trzy'] == 'bandyta':
            wynik += 1
            Odpowiedzi['3'] = 'true'
        if dane['cztery'] == 'spadochron':
            wynik += 1
            Odpowiedzi['4'] = 'true'
        if dane['piec'] == 'mroźna zima':
            wynik += 1
            Odpowiedzi['5'] = 'true'
        if dane['szesc'] == 'kodeks karny':
            wynik += 1
            Odpowiedzi['6'] = 'true'
        if dane['siedem'] == 'łódź podwodna':
            wynik += 1
            Odpowiedzi['7'] = 'true'
        if dane['osiem'] == 'kowboj':
            wynik += 1
            Odpowiedzi['8'] = 'true'
        if dane['dziewiec'] == 'olej':
            wynik += 1
            Odpowiedzi['9'] = 'true'
        if dane['dziesiec'] == 'zakonnica':
            wynik += 1
            Odpowiedzi['10'] = 'true'
        if dane['jedenascie'] == 'lemoniada':
            wynik += 1
            Odpowiedzi['11'] = 'true'
        if dane['dwanascie'] == 'robot':
            wynik += 1
            Odpowiedzi['12'] = 'true'
        if dane['trzynascie'] == 'cyrk':
            wynik += 1
            Odpowiedzi['13'] = 'true'
        if dane['czternascie'] == 'przewodnik':
            wynik += 1
            Odpowiedzi['14'] = 'true'
        if dane['pietnascie'] == 'kuzyn':
            wynik += 1
            Odpowiedzi['15'] = 'true'

        if wynik < 5:
            rezultat = 'bad'
        if 5 <= wynik <= 8:
            rezultat = 'medium'
        if 9 <= wynik <= 12:
            rezultat = 'good'
        if  wynik > 12:
            rezultat = 'very-good'

        if session.get('logged') == True:
            now = datetime.now()
            new_result = results(session['id'], 7, wynik, now)
            db.session.add(new_result)
            db.session.commit()

        return render_template('cwiczenie7wynik.html', test=result, wynik=wynik, odpowiedzi=Odpowiedzi, dane=dane, rezultat=rezultat)
    return render_template('cwiczenie7formularz.html', form=form)

@app.route('/cwiczenie8')
def cwiczenie8():
    return render_template('cwiczenie8.html')

@app.route('/cwiczenie8start')
def cwiczenie8start():
    return render_template('cwiczenie8start.html')

@app.route('/cwiczenie8formularz', methods=["GET", "POST"])
def cwiczenie8formularz():
    form = cwiczenie8Form()
    if form.is_submitted():
        rezultat = ''
        wynik = 0
        result = request.form
        dane = {'jeden': 'Brak odpowiedzi', 'dwa': 'Brak odpowiedzi', 'trzy': 'Brak odpowiedzi', 'cztery': 'Brak odpowiedzi', 'piec': 'Brak odpowiedzi', 'szesc': 'Brak odpowiedzi', 'siedem': 'Brak odpowiedzi', 'osiem': 'Brak odpowiedzi', 'dziewiec': 'Brak odpowiedzi','dziesiec': 'Brak odpowiedzi'}
        dane = request.form.to_dict()
        Odpowiedzi = {'1': 'false', '2': 'false', '3': 'false', '4': 'false', '5': 'false', '6': 'false', '7': 'false', '8': 'false', '9': 'false', '10': 'false'}
        if dane['jeden'] == 'teczka':
            wynik += 1
            Odpowiedzi['1'] = 'true'
        if dane['dwa'] == 'domek letniskowy':
            wynik += 1
            Odpowiedzi['2'] = 'true'
        if dane['trzy'] == 'parkometr':
            wynik += 1
            Odpowiedzi['3'] = 'true'
        if dane['cztery'] == 'urodziny':
            wynik += 1
            Odpowiedzi['4'] = 'true'
        if dane['piec'] == 'wdowa':
            wynik += 1
            Odpowiedzi['5'] = 'true'
        if dane['szesc'] == 'moneta':
            wynik += 1
            Odpowiedzi['6'] = 'true'
        if dane['siedem'] == 'masło':
            wynik += 1
            Odpowiedzi['7'] = 'true'
        if dane['osiem'] == 'marchewka':
            wynik += 1
            Odpowiedzi['8'] = 'true'
        if dane['dziewiec'] == 'puszka':
            wynik += 1
            Odpowiedzi['9'] = 'true'
        if dane['dziesiec'] == 'bieda':
            wynik += 1
            Odpowiedzi['10'] = 'true'

        if wynik < 4:
            rezultat = 'bad'
        if 4 <= wynik <= 7:
            rezultat = 'medium'
        if wynik > 7:
            rezultat = 'good'

        if session.get('logged') == True:
            now = datetime.now()
            new_result = results(session['id'], 8, wynik, now)
            db.session.add(new_result)
            db.session.commit()

        return render_template('cwiczenie8wynik.html', test=result, wynik=wynik, odpowiedzi=Odpowiedzi, dane=dane, rezultat=rezultat)
    return render_template('cwiczenie8formularz.html', form=form)

if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0", port=5030, debug=True)
