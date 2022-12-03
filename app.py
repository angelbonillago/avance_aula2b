from flask import Flask, render_template, request, redirect, url_for,flash,login_required
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

from config import Config
from forms import LoginForm, SignupForm
from models import db
from flask_login import LoginManager
from flask_login import current_user, login_user,logout_user
from models import User



app = Flask(__name__) #me sirve para tener la app de flask
app.config.from_object(Config)
csrf = CSRFProtect()
migrate = Migrate()
#login = LoginManager(app)



db.init_app(app)
migrate.init_app(app, db)


@app.route("/") #ruta raiz
@login_required
def index():
    return render_template("indexCss.html")

@app.route("/hola")
def hola():
    return "<h2>Hola a todos!</h2>"

@app.route("/bienvenido/<nombre>")
def bienvenido(nombre):
    nombre = nombre.upper()
    return render_template("index.html", nombre = nombre)

@app.route("/bienvenido2/")
def bienvenido2():
    nombre = request.args["nombre"]
    nombre = nombre.upper()
    return render_template("index.html", nombre = nombre)

@app.route("/bucles")
def bucles():
    nombres = ["Juan", "Pedro", "Maria"]
    return render_template("bucles.html", nombres = nombres)

@app.route("/login", methods=['GET', 'POST'])
def login():

   #Antes de mandarle el formulario,primero validemos si el usuario ya se logueo

    #if current_user.is_authenticated: #Si esta autenticado,retorna a la vista index 
     #   return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():#valida que el usuario lleno los 2 campos text y password
        #username = form.username.data
        #password = form.password.data
        #print(username, password)
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template("login.html", form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():



    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data       
        print(username, password, email)
        return redirect(url_for('login'))

    return render_template("signup.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))