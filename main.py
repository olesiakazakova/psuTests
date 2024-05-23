import sqlite3
import os
import codecs
from flask import Flask, render_template, url_for, request, session, redirect, abort, g, flash, make_response
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
import re



DATABASE = 'flsite.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'

#print( url_for('оброботчик(имя фцнкции в кот вызывается') ) возвращает url адрес
app=Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))#путь к бд(в раб каталоге)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа"
login_manager.login_message_category = "success"

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

def connect_db():#создание бд\установление соежинения
    conn = sqlite3.connect(app.config['DATABASE'])#путь рассположения бд
    conn.row_factory = sqlite3.Row#записи бд будут ввиде словаря, а не кортежей
    return conn#возвращает установленное соединение

def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/")
@login_required
def index():
    return render_template('index.html', menu = dbase.getMenu(), post=dbase.getPostsAnonce(current_user.get_id()), title= 'psuTests')

@app.route("/help")
def help():
    if current_user.is_authenticated:
        return render_template('help2.html', menu=dbase.getMenu(), title='Инструкция')

    return render_template('help.html', menu = dbase.getMenu(), title= 'Инструкция')

def process_text(text):

    def process_line(line):
        line = line.strip()


        if "==" in line:
            return line
        elif re.match(r"^\d+[)]\s*\w+", line):

            return line
        elif re.match(r"[а-яА-Я][)]\s*\w+", line):


            match = re.match(r"^[а-яА-Я][)]\s*[а-яА-Я0-9,\s,\-,\–]*\*+$", line)

            if match:
                return line.strip()[:-1]
            else:
                return line[0] + ")"
        elif re.match(r"^\[.*\]$", line):
            return line.strip("[]")
        return None


    lines = text.split("\n")
    processed_lines = [process_line(line) for line in lines]
    processed_lines = [line for line in processed_lines if line != None]


    result =  "\n".join(processed_lines)

    return result


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        if len(request.form['post']) > 10:
            post=process_text(request.form['post'])
            res = dbase.addPost(current_user.get_id(),request.form['classes'], request.form['themes'], post)
            if not res:
                flash("Ошибка добавления заданий", "error")
                return redirect(url_for('upload'))
            flash("Задания добавлены успешно", "success")
        else:
            flash("Ошибка добавления заданий", "error")

    return render_template('load.html', menu=dbase.getMenu(), title="Загрузка заданий")

@app.route("/post/<int:id_post>")
@login_required
def showPost(id_post):
    classes, themes, post = dbase.getPost(id_post)
    if not classes or not themes:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), classes=classes, title= themes, post=post)

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("index"))

        flash("Неверный логин/пароль", "error")

    return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        session.pop('_flashes', None)
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
                and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")

    return render_template("register.html", menu=dbase.getMenu(), title="Регистрация")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", menu=dbase.getMenu(), title="Профиль")

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=dbase.getMenu()), 404

if __name__ == "__main__" :
    app.run(debug=True) #после завершения написания сайта поменять на false!!!
