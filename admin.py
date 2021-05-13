from flask import Blueprint, render_template
from werkzeug.utils import redirect, secure_filename

from data import db_session
from data.news import News
from forms.news import NewsForm

admin = Blueprint('admin', 'admin')

@admin.route('/admin/news')
def get_news_list():
    db_sess = db_session.create_session()
    data = db_sess.query(News)
    return render_template("admin/news.html", news=data, title="Управление Новостями")


@admin.route('/admin/news_item/new', methods=['GET', 'POST'])
def new_news_item():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        filename = secure_filename(form.image.data.filename)
        form.image.data.save('uploads/'+filename)
        news = News(form.title.data, form.content.data, '/img/'+filename, 1)
        db_sess.add(news)
        db_sess.commit()
        return redirect(f"/admin/news")
    return render_template('admin/news_item.html', title='Новая Новость', form=form)

@admin.route('/admin/products')
def get_products_list():
    return "products_list_page"

@admin.route('/admin/users')
def get_users_list():
    return "users_list_page"