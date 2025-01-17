from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.inventory import NewsForm
from forms.user import RegisterForm, LoginForm
from data.inventory import Inventory
from data.users import User
from data import db_session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'home_str'

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/inventory/<id>/more_detailed')
@login_required
def more_detailed(id):
    db_sess = db_session.create_session()
    user = db_sess.query(Inventory).filter(Inventory.id == id).all()
    return render_template('more_detailed.html', n=user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/index")


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/inventory', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        inventory = Inventory()
        inventory.title = form.title.data
        inventory.content = form.content.data
        inventory.is_rented = form.is_private.data
        current_user.inventory.append(inventory)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/index')
    return render_template('inventory.html', title='Добавление позиции', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Inventory).filter(Inventory.id == id, Inventory.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/index')


@app.route('/inventory/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Inventory).filter(Inventory.id == id, Inventory.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_rented
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Inventory).filter(Inventory.id == id, Inventory.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_rented = form.is_private.data
            db_sess.commit()
            return redirect('/index')
        else:
            abort(404)
    return render_template('inventory.html', title='Редактирование новости', form=form)


@app.route("/index")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(Inventory).filter((Inventory.user == current_user) | (Inventory.is_rented != False))
    else:
        news = db_sess.query(Inventory).filter(Inventory.is_rented != False)
    return render_template("index.html", inventory=news)


@app.route('/reqister', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.admin = 'False'
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/index")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
