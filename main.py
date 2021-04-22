from flask import Flask, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect

from flask_restful import  abort, Api
from api import news_resource
from data import db_session, api
from data.news import News
from data.users import User
from data.comments import Comments
from forms.comment import CommentForm

from forms.register import RegisterForm
from forms.login import LoginForm

app = Flask(__name__)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

# для списка объектов
api.add_resource(news_resource.NewsListResource, '/api/v2/news')
# для одного объекта
api.add_resource(news_resource.NewsResource, '/api/v2/news/<int:news_id>')

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news, title="Записи в блоге")

@app.route("/news")
def news():
    db_sess = db_session.create_session()
    data = db_sess.query(News)
    return render_template("news.html", news=data, title="Новости")

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


from flask import make_response,jsonify

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def main():
    db_session.global_init("db/comments.sqlite")

    db_sess = db_session.create_session()
    db_sess.add(News('Test', 'Text', '', 1))
    db_sess.commit()
    for user in db_sess.query(User).all():
        print(user)
    users = db_sess.query(User).filter(User.about.contains('пользоват'), User.id != 1, User.id % 2 != 0).all()

    for user in users:
        print(user)

    #app.register_blueprint(api.blueprint)
    app.run()

if __name__ == '__main__':

    main()