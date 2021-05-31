from flask import Blueprint, render_template
from flask_login import login_required, current_user
from werkzeug.utils import redirect, secure_filename

from data import db_session
from data.categories import Categories
from data.news import News
from data.product import Product
from forms.categories import CategoriesForm
from forms.delete_confirm import DeleteForm
from forms.news import NewsForm
from forms.product import ProductForm

admin = Blueprint('admin', 'admin')

def admin_protect(func):
    def decoreated_func(*args, **kwargs):
        if current_user.role == 'admin':
            return func(*args, **kwargs)
        else:
            return redirect('/')
    return decoreated_func


@admin.route('/admin/news', endpoint='get_news_list')
@admin_protect
@login_required
def get_news_list():
    db_sess = db_session.create_session()
    data = db_sess.query(News)
    return render_template("admin/news.html", news=data, title="Управление Новостями")

@admin.route('/admin/news_item/new',
             endpoint='new_news_item', methods=['GET', 'POST'])
@admin_protect
@login_required
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

@admin.route('/admin/news_item/<int:id>',
             endpoint='edit_news_item', methods=['GET', 'POST'])
@admin_protect
@login_required
def edit_news_item(id):
    form = NewsForm()
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(id)

    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        if filename != '' and news.image != '/img/'+filename:
            form.image.data.save('uploads/'+filename)
            news.image = '/img/' + filename
        news.title = form.title.data
        news.content = form.content.data
        db_sess.commit()
        return redirect('/admin/news')
    else:
        form.title.data = news.title
        form.content.data = news.content
        form.image.filename = news.image
    return render_template('admin/news_item.html', title='Редактировать Новость', form=form)

@admin.route('/admin/news_item/delete/<int:id>',
             endpoint='delete_news_item', methods=['GET', 'POST'])
@admin_protect
@login_required
def delete_news_item(id):
    form = DeleteForm()
    if not form.validate_on_submit():
        form.id.data = id
        return render_template('admin/delete_element.html', title='Удалить Новость', form=form)
    elif form.confirm.data == True:
        del_id = form.id.data
        db_sess = db_session.create_session()
        news = db_sess.query(News).get(id)
        db_sess.delete(news)
        db_sess.commit()
    return redirect('/admin/news')

@admin.route('/admin/products',
             endpoint='get_products_list')
@admin_protect
@login_required
def get_products_list():
    db_sess = db_session.create_session()
    data = db_sess.query(Product)
    return render_template("admin/products.html", products=data, title="Управление Товарами")

@admin.route('/admin/products_item/new',
             endpoint='new_products_item', methods=['GET', 'POST'])
@admin_protect
@login_required
def new_products_item():
    form = ProductForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        filename = secure_filename(form.image.data.filename)
        form.image.data.save('uploads/'+filename)
        product = Product(form.title.data, form.content.data,
                          '/img/'+filename, form.price.data,
                          form.is_featured.data)
        db_sess.add(product)
        db_sess.commit()
        return redirect(f"/admin/products")
    return render_template('admin/products_item.html', title='Новый Товар', form=form)

@admin.route('/admin/categories', endpoint='get_categories_list')
@admin_protect
@login_required
def get_categories_list():
    db_sess = db_session.create_session()
    data = db_sess.query(Categories)
    return render_template("admin/categories.html", categories=data, title="Управление Категориями")

@admin.route('/admin/categories_item/new',
             endpoint='new_categories_item', methods=['GET', 'POST'])
@admin_protect
@login_required
def new_categories_item():
    form = CategoriesForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        category = Categories(form.title.data, form.content.data)
        db_sess.add(category)
        db_sess.commit()
        return redirect(f"/admin/categories")
    return render_template('admin/categories_item.html', title='Новая Категория', form=form)


@admin.route('/admin/users',
             endpoint='get_users_list')
@admin_protect
@login_required
def get_users_list():
    return "users_list_page"