from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, RadioField
from wtforms.validators import EqualTo, DataRequired, Length, ValidationError


class cwiczenie1Form(FlaskForm):
    jeden = StringField('1')
    dwa = StringField('2')
    trzy = StringField('3')
    cztery = StringField('4')
    piec = StringField('5')
    szesc = StringField('6')
    siedem = StringField('7')
    osiem = StringField('8')
    dziewiec = StringField('9')
    dziesiec = StringField('10')
    submit = SubmitField('Zakończ')


class cwiczenie2Form(FlaskForm):
    jeden = StringField('1')
    dwa = StringField('2')
    trzy = StringField('3')
    cztery = StringField('4')
    piec = StringField('5')
    szesc = StringField('6')
    siedem = StringField('7')
    osiem = StringField('8')
    dziewiec = StringField('9')
    submit = SubmitField('Zakończ')


class cwiczenie3Form(FlaskForm):
    jeden = StringField('1')
    dwa = StringField('2')
    trzy = StringField('3')
    cztery = StringField('4')
    piec = StringField('5')
    szesc = StringField('6')
    siedem = StringField('7')
    osiem = StringField('8')
    dziewiec = StringField('9')
    dziesiec = StringField('10')
    submit = SubmitField('Zakończ')


class cwiczenie4Form(FlaskForm):
    jeden = StringField('1')
    dwa = StringField('2')
    trzy = StringField('3')
    cztery = StringField('4')
    piec = StringField('5')
    szesc = StringField('6')
    siedem = StringField('7')
    osiem = StringField('8')
    dziewiec = StringField('9')
    dziesiec = StringField('10')
    submit = SubmitField('Zakończ')


class cwiczenie5Form(FlaskForm):
    pociag =  RadioField('grupa1', choices=[('torba','1'),('zegar','2'),('staruszek','3')])
    drabina =  RadioField('grupa2', choices=[('jaskinia','1'),('mikrofon','2'),('fotel','3')])
    submit = SubmitField('Zakończ')


class cwiczenie6Form(FlaskForm):
    jeden = StringField('1')
    dwa = StringField('2')
    trzy = StringField('3')
    cztery = StringField('4')
    piec = StringField('5')
    szesc = StringField('6')
    siedem = StringField('7')
    osiem = StringField('8')
    dziewiec = StringField('9')
    dziesiec = StringField('10')
    jedenascie = StringField('11')
    dwanascie = StringField('12')
    trzynascie = StringField('13')
    czternascie = StringField('14')
    pietnascie = StringField('15')
    submit = SubmitField('Zakończ')


class cwiczenie7Form(FlaskForm):
    jeden = StringField('1')
    dwa = StringField('2')
    trzy = StringField('3')
    cztery = StringField('4')
    piec = StringField('5')
    szesc = StringField('6')
    siedem = StringField('7')
    osiem = StringField('8')
    dziewiec = StringField('9')
    dziesiec = StringField('10')
    jedenascie = StringField('11')
    dwanascie = StringField('12')
    trzynascie = StringField('13')
    czternascie = StringField('14')
    pietnascie = StringField('15')
    submit = SubmitField('Zakończ')


class cwiczenie8Form(FlaskForm):
    jeden = StringField('1')
    dwa = StringField('2')
    trzy = StringField('3')
    cztery = StringField('4')
    piec = StringField('5')
    szesc = StringField('6')
    siedem = StringField('7')
    osiem = StringField('8')
    dziewiec = StringField('9')
    dziesiec = StringField('10')
    submit = SubmitField('Zakończ')


class loginForm(FlaskForm):
    login = StringField('Login', [DataRequired(message='Pole obowiązkowe')])
    password = PasswordField('Hasło', [DataRequired(message='Pole obowiązkowe')])
    submit = SubmitField('Zaloguj')


class registerForm(FlaskForm):
    login = StringField('Login', [Length(min=4, max=20, message='Login musi mieć długość pomiędzy 4, a 20 znaki'),
                                  DataRequired(message='Pole obowiązkowe')])

    name = StringField('Imię', [Length(min=3, max=20, message='Imię musi mieć długość pomiędzy 3, a 20 znaki'),
                                DataRequired(message='Pole obowiązkowe')])
    password = PasswordField('Hasło', [DataRequired(message='Pole obowiązkowe')])
    repeat_password = PasswordField('Powtórz hasło', [EqualTo('password', message='Hasła muszą do siebie pasować'),
                                                      DataRequired(message='Pole obowiązkowe')])
    submit = SubmitField('Zarejestruj')
