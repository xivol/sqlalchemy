import os

from PIL import Image, ImageEnhance
from flask import Flask, render_template, request, Blueprint, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort
from werkzeug.utils import redirect

from admin import admin
from data import db_session
from data.categories import Categories
from data.news import News
from data.order import Order
from data.product import Product
from data.users import User
from data.comments import Comments
from forms.comment import CommentForm

from forms.register import RegisterForm
from forms.login import LoginForm

app = Flask(__name__)
app.register_blueprint(admin)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def make_dark_img(img_name, factor):
    im = Image.open('./uploads/' + img_name)
    enhancer = ImageEnhance.Brightness(im)
    im_output = enhancer.enhance(factor)
    dark_im = ''.join(img_name.split('.')[:-1] + ['_featured', '.', img_name.split('.')[-1]])
    im_output.save('./uploads/' + dark_im)
    return dark_im

@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = list(db_sess.query(News))
    for item in news:
        item.feature_image = '/img/' + make_dark_img(os.path.split(item.image)[-1], 0.3)
    products = db_sess.query(Product).filter(Product.is_featured == True)
    return render_template("index.html", news=news, products=products, title="Добро пожаловать")

@app.route("/news")
def news():
    db_sess = db_session.create_session()
    data = db_sess.query(News)
    return render_template("news.html", news=data, title="Новости")

@app.route('/products')
def product():
    category = request.args.get("category", None)
    db_sess = db_session.create_session()
    cat = db_sess.query(Categories)
    if not category:
        data = db_sess.query(Product)
        return render_template("product.html",
                               products=data,
                               categories=cat,
                               title="Товары")
    else:
        data = db_sess.query(Product).filter(Product.categories.title == category)
        for d in data:
            print(d.categories)
        return render_template("product.html",
                               products=data,
                               categories=cat,
                               title="Товары")

@app.route("/comment_like/<int:id>", methods=['POST'])
def comment_like(id):
    db_sess = db_session.create_session()
    data = db_sess.query(Comments).get(id)
    data.likes += 1
    result = data.likes
    db_sess.commit()
    return make_response(str(result))


@app.route("/news/<int:id>", methods=['GET', 'POST'])
def news_item(id):
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        form = CommentForm()
        if form.validate_on_submit():
            comm = Comments()
            comm.connected_to_id = id
            comm.table_name = News.__tablename__
            comm.author_id = current_user.id
            comm.text = form.text.data
            db_sess.add(comm)
            db_sess.commit()
    else:
        form = None

    data = db_sess.query(News).get(id)
    comments = db_sess.query(Comments).filter(Comments.connected_to_id == id,
                                              Comments.table_name == News.__tablename__)

    return render_template("news_item.html", news=data, title=data.title, comments=comments, form=form)

@app.route("/products/<int:id>", methods=['GET', 'POST'])
def product_item(id):
    db_sess = db_session.create_session()
    data = db_sess.query(Product).get(id)
    # comments = db_sess.query(Comments).filter(Comments.connected_to_id == id,
    #                                           Comments.table_name == News.__tablename__)

    return render_template("product.item.html", item=data, title=data.title)


@app.route("/order")
def order():
    db_sess = db_session.create_session()
    data_orders = db_sess.query(Order)
    return render_template("order.html", news=data_orders, title="Заказы")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")

@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('uploads', path)

from flask import make_response, jsonify


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    if not os.path.exists("db"):
        os.makedirs("db")
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    db_session.global_init("db/website.sqlite")
    db_sess = db_session.create_session()
    try:
        admin = User('Admin', 'Admin', 'admin@mail.ru', 'admin')
        admin.set_password('admin')
        db_sess.add(admin)
        db_sess.commit()
    except:
        db_sess.rollback()

    for user in db_sess.query(User).all():
        print(user)

    return app


if __name__ == '__main__':
    main().run()
