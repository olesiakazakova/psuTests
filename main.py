import sqlite3
import os
import codecs
from flask import Flask, render_template, url_for, request, session, redirect, abort, g, flash, make_response #импорт классов
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin

DATABASE = '/tmp/flsite.db'
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


def simple_test(ans):
    line = ""
    itog = ""
    var_answers = "абвгдежзийклмнопрстуфхцычшщая"
    line = ans.readline()
    while True:
        line = ans.readline()

        if not line:
            break

        if line[0].lower() in var_answers and line[1] == ")" and line[-2] == "*":
            itog += line[0] + line[1] + "*\n"
        else:
            itog += line[0] + line[1] + "\n"

    itog = itog.rstrip()

    return itog


def vstavka_slova_predlozhenia(ans):
    itog = ""
    while True:
        line = ans.readline()

        if not line:
            break
        if line[0] == "[" and (line[-1] == "]" or line[-2] == "]"):
            if line[-2] == "]":
                for simv in range(1, len(line) - 2):
                    itog += line[simv]
            else:
                for simv in range(1, len(line) - 1):
                    itog += line[simv]

    return itog


def sootv_func(ans):
    itog = {}
    simv = 0

    while True:
        first_word = ""
        second_word = ""
        line = ans.readline()

        if not line:
            break

        if "==" in line:
            for simv in range(len(line)):
                if line[simv] == "=":
                    simv += 2
                    break
                first_word += line[simv]

            if line[-1] == "\n":
                for simv1 in range(simv, len(line) - 1):
                    second_word += line[simv1]
            else:
                for simv1 in range(simv, len(line)):
                    second_word += line[simv1]

            itog[first_word] = second_word

    return itog


##############################################
def vstav():
    questvst = open("quest.txt", "r", encoding="utf-16")

    linevst = questvst.readline()

    if linevst[2] == "в" and linevst[3] == "с":
        itog.write(linevst)
        questvst.close()
        questvst = open("quest.txt", "r", encoding="utf-16")
        vst = vstavka_slova_predlozhenia(questvst)
        itog.write(vst)
    else:
        questvst.close()


def smpl():
    questsmpl = open("quest.txt", "r", encoding="utf-16")
    linesmpl = questsmpl.readline()

    if len(linesmpl) >= 4 and linesmpl[2].lower() == "в" and linesmpl[3].lower() == "ы":
        itog.write(linesmpl)
        questsmpl.close()
        questsmpl = open("quest.txt", "r", encoding="utf-16")
        smpl = simple_test(questsmpl)
        itog.write(smpl)
    else:
        questsmpl.close()


def sootv():
    questsootv = open("quest.txt", "r", encoding="utf-16")
    linesootv = questsootv.readline()

    if len(linesootv) >= 4 and linesootv[2].lower() == "у" and linesootv[3].lower() == "с":
        itog.write(linesootv)
        questsootv.close()
        questsootv = open("quest.txt", "r", encoding="utf-16")
        sotv = sootv_func(questsootv)
        for i, (key, value) in enumerate(sotv.items()):
            if i == len(sotv) - 1:
                itog.write(f"{key} == {value}")
            else:
                itog.write(f"{key} == {value}\n")

    else:
        questsootv.close()

    ###############################################


# a = open("example_simple.txt", "r",encoding = "utf-8")
# g = simple_test(a)
# print (g)
##print("------------------------")
##a.close()
##
##
# a = open("example_vstavka.txt", "r",encoding = "utf-8")
# b=vstavka_slova_predlozhenia(a)
# print(b)
##a.close()
##print("------------------------")
##a = open("example_sootv.txt", "r",encoding = "utf-8")
##c = sootv(a)
##print(c.items())

def parse(text):
    global itog
    test = open("full_test.txt", "w", encoding="utf-8")
    test.write(text)
    test.close()
    test = open("full_test.txt", "r", encoding="utf-8")
    quest = open("quest.txt", "w+", encoding="utf-16")
    itog = open("itog.txt", "w+", encoding="utf-16")
    k = 1
    g = 0
    line = ""

    while True:
        g += 1
        line = test.readline()
        if not line:
            break

        print(g)
        if line[0].isdigit() and line[1] == ")"  and k != 1:
            quest.close()
            vstav()
            smpl()
            sootv()
            itog.write("\n")

            quest.close()
            open("quest.txt", "w+", encoding="utf-16").close()
            quest = open("quest.txt", "w+", encoding="utf-16")
            quest.write(line)
            k = 1
        else:
            quest.write(line)
            k = 0
    # Открываем файл в режиме чтения и записи ('rb+' для бинарного режима)
    quest.close()
    vstav()
    smpl()
    sootv()
    itog.write("\n")
    quest.close()
    itog.close()
    itog = open("itog.txt", "r", encoding="utf-16")
    p = itog.read()
    itog.close()
    print(g)
    # quest = open("quest.txt","w+",encoding = "utf-16")
    # d = simple_test(quest)
    # itog.write(d)
    # print(d)

    # vstav()

    # g = str(input())
    test.close()
    os.remove("full_test.txt")
    os.remove("quest.txt")
    os.remove("itog.txt")
    return p


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        if len(request.form['post']) > 10:
            post=parse(request.form['post'])
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
    app.run(debug=True) #после завершения написания сайта поменять на false!!! (чтобы ошибки не были видны пользователю)
