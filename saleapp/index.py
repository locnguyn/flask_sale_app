import math

from flask import render_template, request, redirect
from models import UserRole
import dao
from saleapp import app, login
from flask_login import login_user


@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('category_id')
    page = request.args.get('page')

    prods = dao.load_products(kw=kw, cate_id=cate_id, page=page)
    total = dao.count_product()

    return render_template('index.html', products=prods,
                           pages=math.ceil(total/app.config['PAGE_SIZE']))


@app.route('/login', methods=['get', 'post'])
def process_login_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        if username.__eq__('admin') and password.__eq__('123'):
            return redirect('/')
        else:
            err_msg = 'Tên đăng nhập hoặc mật khẩu không hợp lệ!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def process_login_admin():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username, password, UserRole.ADMIN)
    if u:
        login_user(user=u)

    return redirect('/admin')


@app.context_processor
def common_attributes():
    return {
        'categories': dao.load_categories()
    }


@login.user_loader
def user_load(id):
    return dao.get_user_by_id(id)


if __name__ == '__main__':
    with app.app_context():
        from saleapp import admin
        app.run(debug=True)
