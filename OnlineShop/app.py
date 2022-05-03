from tkinter import E
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_uploads import UploadSet, configure_uploads, IMAGES
import timeit
import datetime
from flask_mail import Mail, Message
import os
from wtforms.fields.html5 import EmailField

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/image/product'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Kết nối dữ liệu
mysql = MySQL()
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'abd_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql.init_app(app)

# Đã đăng nhập
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('login'))

    return wrap
def is_manager(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['admin_role'] == 'manager':
            return f(*args, *kwargs)
        else:
            return redirect(url_for('admin'))
    return wrap

# Chưa đăng nhập
def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('index'))
        else:
            return f(*args, *kwargs)

    return wrap

# Đã đăng nhập bằng admin
def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('admin_login'))

    return wrap

# Chưa đăng chập admin
def not_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return redirect(url_for('admin'))
        else:
            return f(*args, *kwargs)

    return wrap


def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped

# Lọc danh sách sản phẩm
def content_based_filtering(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))  # getting id row
    data = cur.fetchone()  # get row info
    data_cat = data['category']  # get id category ex shirt
    print('Showing result for Product Id: ' + product_id)
    category_matched = cur.execute("SELECT * FROM products WHERE category=%s", (data_cat,))  # get all shirt category
    print('Total product matched: ' + str(category_matched))
    cat_product = cur.fetchall()  # get all row
    cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))  # id level info
    id_level = cur.fetchone()
    recommend_id = []
    cate_level = ['dell', 'asus', 'apple', 'lenovo', 'gaming', 'office', 'acer', 'screen_4k', 'screen_2k', 'bluetooth', 'cable', 'screen_22', 'screen_24', 'screen_gaming', 'screen_graphics', 'new_product', 'logitech', 'razer', 'edra']
    for product_f in cat_product:
        cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_f['id'],))
        f_level = cur.fetchone()
        match_score = 0
        if f_level['product_id'] != int(product_id):
            for cat_level in cate_level:
                if f_level[cat_level] == id_level[cat_level]:
                    match_score += 1
            if match_score == 19:
                recommend_id.append(f_level['product_id'])
    print('Total recommendation found: ' + str(recommend_id))
    if recommend_id:
        cur = mysql.connection.cursor()
        placeholders = ','.join((str(n) for n in recommend_id))
        query = 'SELECT * FROM products WHERE id IN (%s)' % placeholders
        cur.execute(query)
        recommend_list = cur.fetchall()
        return recommend_list, recommend_id, category_matched, product_id
    else:
        return ''

# Lấy dữ liệu cho trang chủ
@app.route('/')
def index():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    
    # laptop
    values = 'laptop'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 8", (values,))
    laptop = cur.fetchall()
    # mouse
    values = 'mouse'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 8", (values,))
    mouse = cur.fetchall()
    # keyboard
    values = 'keyboard'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 8", (values,))
    keyboard = cur.fetchall()
     # screen
    values = 'screen'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 8", (values,))
    screen = cur.fetchall()
    # Close Connection
    cur.close()
    return render_template('home.html', laptop=laptop, mouse = mouse, keyboard = keyboard, screen=screen, form=form)

# Form Đăng nhập
class LoginForm(Form):  
    username = StringField('', [validators.length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})

# Đăng nhập
@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['password']
            uid = data['id']
            name = data['name']

            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['uid'] = uid
                session['s_name'] = name
                x = '1'
                cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))

                return redirect(url_for('index'))

            else:
                flash('Sai mật khẩu', 'danger')
                return render_template('login.html', form=form)

        else:
            flash('Tài khoản chưa đăng ký', 'danger')
            # Close connection
            cur.close()
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

# Đăng xuất
@app.route('/out')
def logout():
    if 'uid' in session:
        # Create cursor
        cur = mysql.connection.cursor()
        uid = session['uid']
        x = '0'
        cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        session.clear()
        flash('Bạn đã đăng xuất!!', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('login'))

# Form đăng ký
class RegisterForm(Form):
    name = StringField('', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Họ và tên'})
    username = StringField('', [validators.length(min=3, max=25)], render_kw={'placeholder': 'Username'})
    email = EmailField('', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})
    mobile = StringField('', [validators.length(min=10, max=15)], render_kw={'placeholder': 'Số điện thoại'})

# Đăng ký
@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        mobile = form.mobile.data

        # Create Cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password, mobile) VALUES(%s, %s, %s, %s, %s)",
                    (name, email, username, password, mobile))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Bạn đã đăng ký thành công', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


class MessageForm(Form):  
    body = StringField('', [validators.length(min=1)], render_kw={'autofocus': True})


@app.route('/chatting/<string:id>', methods=['GET', 'POST'])
def chatting(id):
    if 'uid' in session:
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.connection.cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM users WHERE id=%s" , [id])
        l_data = cur.fetchone()
        
        if get_result > 0:
            session['name'] = l_data['name']
            uid = session['uid']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO messages(body, msg_by, msg_to) VALUES(%s, %s, %s)",
                            (txt_body, id, uid))
                # Commit cursor
                mysql.connection.commit()

            # Get users
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            cur.execute("SELECT * FROM users WHERE id=%s" , [uid])
            u_role = cur.fetchone()
            role = u_role['role']
            # Close Connection
            cur.close()
            return render_template('chat_room.html', users=users,role = role, form=form)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/chats', methods=['GET', 'POST'])
def chats():
    if 'lid' in session:
        id = session['lid']
        uid = session['uid']
        # Create cursor
        cur = mysql.connection.cursor()
        # Get message
        cur.execute("SELECT * FROM messages WHERE (msg_by=%s AND msg_to=%s) OR (msg_by=%s AND msg_to=%s) "
                    "ORDER BY id ASC", (id, uid, uid, id))
        chats = cur.fetchall()
       
        # Close Connection
        cur.close()
        return render_template('chats.html', chats=chats, )
    else:
        return redirect(url_for('login'))

# Form đặt hàng
class OrderForm(Form): 
    name = StringField('', [validators.length(min=1), validators.DataRequired()], render_kw={'autofocus': True, 'placeholder': 'Họ và tên'})
    mobile_num = StringField('', [validators.length(min=1), validators.DataRequired()],render_kw={'autofocus': True, 'placeholder': 'Số điện thoại'})
    quantity = SelectField('', [validators.DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    order_place = StringField('', [validators.length(min=1), validators.DataRequired()], render_kw={'placeholder': 'Địa chỉ'})
    total = StringField('', [], render_kw={})



# Danh sách Laptop
@app.route('/laptop', methods=['GET', 'POST'])
def laptop():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'laptop'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        total = form.total.data
       
        # Create Cursor
        curs = mysql.connection.cursor()
        curs.execute("SELECT pName FROM products WHERE id=%s ", (pid,))
        pName = curs.fetchall()
        pName = pName[0]['pName']

        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, pName, mobile, oplace, quantity, total, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name,pName, mobile, order_place, quantity, total, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname,pName, mobile, oplace, quantity, total, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                         (pid, name,pName, mobile, order_place, quantity, total, now_time))
        

        curs.execute("SELECT available FROM products WHERE id=%s ", (pid,))
        quantity_old = curs.fetchall()
        quantity_old = quantity_old[0]['available']
        quantity_new = int(quantity_old) - int(quantity)
        # Update so luong sau khi dat hang
        curs.execute("UPDATE products SET available = %s WHERE id = %s", (quantity_new, pid))
        # Commit cursor
        mysql.connection.commit()
        # Close Connection
        curs.close()
       

        flash('Order successful', 'success')
        return render_template('laptop.html', laptop=products,form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, tshirts=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        if 'uid' in session:
            uid = session['uid']
            curso.execute("SELECT * FROM users WHERE id=%s", (uid,))
            u = curso.fetchall()
            u = u[0]
        else:
            u ={'name': '', 'mobile': '', 'order_place': ''}
        
        return render_template('order_product.html', x=x, tshirts=product, user = u,  form=form)
    return render_template('laptop.html', laptop=products, form=form)

# Danh sách Chuột
@app.route('/mouse', methods=['GET', 'POST'])
def mouse():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'mouse'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        total = form.total.data
       
        # Create Cursor
        curs = mysql.connection.cursor()
        curs.execute("SELECT pName FROM products WHERE id=%s ", (pid,))
        pName = curs.fetchall()
        pName = pName[0]['pName']

        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, pName, mobile, oplace, quantity, total, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name,pName, mobile, order_place, quantity, total, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname,pName, mobile, oplace, quantity, total, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                         (pid, name,pName, mobile, order_place, quantity, total, now_time))
        

        curs.execute("SELECT available FROM products WHERE id=%s ", (pid,))
        quantity_old = curs.fetchall()
        quantity_old = quantity_old[0]['available']
        quantity_new = int(quantity_old) - int(quantity)
        # Update so luong sau khi dat hang
        curs.execute("UPDATE products SET available = %s WHERE id = %s", (quantity_new, pid))
        # Commit cursor
        mysql.connection.commit()
        # Close Connection
        curs.close()

        flash('Order successful', 'success')
        return render_template('mouse.html', mouse=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, tshirts=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        if 'uid' in session:
            uid = session['uid']
            curso.execute("SELECT * FROM users WHERE id=%s", (uid,))
            u = curso.fetchall()
            u = u[0];
        else:
            u ={'name': '', 'mobile': '', 'order_place': ''}
        return render_template('order_product.html', x=x, tshirts=product, user = u,  form=form)
    return render_template('mouse.html', mouse=products, form=form)

# Danh sách bàn phím
@app.route('/keyboard', methods=['GET', 'POST'])
def keyboard():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'keyboard'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        total = form.total.data
       
        # Create Cursor
        curs = mysql.connection.cursor()
        curs.execute("SELECT pName FROM products WHERE id=%s ", (pid,))
        pName = curs.fetchall()
        pName = pName[0]['pName']

        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, pName, mobile, oplace, quantity, total, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name,pName, mobile, order_place, quantity, total, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname,pName, mobile, oplace, quantity, total, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                         (pid, name,pName, mobile, order_place, quantity, total, now_time))
        

        curs.execute("SELECT available FROM products WHERE id=%s ", (pid,))
        quantity_old = curs.fetchall()
        quantity_old = quantity_old[0]['available']
        quantity_new = int(quantity_old) - int(quantity)
        # Update so luong sau khi dat hang
        curs.execute("UPDATE products SET available = %s WHERE id = %s", (quantity_new, pid))
        # Commit cursor
        mysql.connection.commit()
        # Close Connection
        curs.close()

        flash('Order successful', 'success')
        return render_template('keyboard.html', keyboard=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, tshirts=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        if 'uid' in session:
            uid = session['uid']
            curso.execute("SELECT * FROM users WHERE id=%s", (uid,))
            u = curso.fetchall()
            u = u[0]
        else:
            u ={'name': '', 'mobile': '', 'order_place': ''}
        return render_template('order_product.html', x=x, tshirts=product, user = u,  form=form)
    return render_template('keyboard.html', keyboard=products, form=form)

# Danh sách màn hinh
@app.route('/screen', methods=['GET', 'POST'])
def screen():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'screen'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        total = form.total.data
       
        # Create Cursor
        curs = mysql.connection.cursor()
        curs.execute("SELECT pName FROM products WHERE id=%s ", (pid,))
        pName = curs.fetchall()
        pName = pName[0]['pName']

        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, pName, mobile, oplace, quantity, total, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name,pName, mobile, order_place, quantity, total, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname,pName, mobile, oplace, quantity, total, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                         (pid, name,pName, mobile, order_place, quantity, total, now_time))
        

        curs.execute("SELECT available FROM products WHERE id=%s ", (pid,))
        quantity_old = curs.fetchall()
        quantity_old = quantity_old[0]['available']
        quantity_new = int(quantity_old) - int(quantity)
        # Update so luong sau khi dat hang
        curs.execute("UPDATE products SET available = %s WHERE id = %s", (quantity_new, pid))
        # Commit cursor
        mysql.connection.commit()
        # Close Connection
        curs.close()

        flash('Order successful', 'success')
        return render_template('screen.html', screen=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, tshirts=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        if 'uid' in session:
            uid = session['uid']
            curso.execute("SELECT * FROM users WHERE id=%s", (uid,))
            u = curso.fetchall()
            u = u[0];
        else:
            u ={'name': '', 'mobile': '', 'order_place': ''}
        return render_template('order_product.html', x=x, tshirts=product, user = u,  form=form)
    return render_template('screen.html', screen=products, form=form)



@app.route('/admin_login', methods=['GET', 'POST'])
@not_admin_logged_in
def admin_login():
    if request.method == 'POST':
        # GEt user form
        username = request.form['email']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM admin WHERE email=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['password']
            uid = data['id']
            name = data['fullName']
            role = data['type']
            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['admin_logged_in'] = True
                session['admin_uid'] = uid
                session['admin_name'] = name
                session['admin_role'] = role

                return redirect(url_for('admin'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('pages/login.html')

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('pages/login.html')
    return render_template('pages/login.html')


@app.route('/admin_out')
def admin_logout():
    if 'admin_logged_in' in session:
        session.clear()
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin'))


@app.route('/admin', methods=['GET', 'POST'])
@is_admin_logged_in
def admin():
    curso = mysql.connection.cursor()
    if request.method == 'POST':
        query = request.form['search']
        standardlize ="%"+request.form['search']+"%"
        num_rows = curso.execute("SELECT * FROM products where products.pName LIKE %s or products.pCode LIKE %s", (standardlize,standardlize))
        result = curso.fetchall()
        flash('Search results for: {}'.format(query),'success')
        return render_template('pages/index_admin.html', result=result, row=num_rows)

    else:    
        num_rows = curso.execute("SELECT * FROM products")
        result = curso.fetchall()
        order_rows = curso.execute("SELECT * FROM orders")
        users_rows = curso.execute("SELECT * FROM users")
        admin_rows = curso.execute("SELECT * FROM admin")
        return render_template('pages/index_admin.html', result=result, row=num_rows, order_rows=order_rows,
                    users_rows=users_rows, admin_rows= admin_rows)


@app.route('/orders', methods=['GET', 'POST'])
@is_admin_logged_in
def orders():
    curso = mysql.connection.cursor()
    if request.method == 'POST':
        query = request.form['search']
        standardlize ="%"+request.form['search']+"%"
        num_rows = curso.execute("SELECT * FROM orders where id = %s or mobile LIKE %s", (query,standardlize))
        result = curso.fetchall()
        flash('Search results for: {}'.format(query),'success')
        return render_template('pages/all_orders.html', result=result, row=num_rows)

    else:    
        num_rows = curso.execute("SELECT * FROM products")
        order_rows = curso.execute("SELECT * FROM orders")
        result = curso.fetchall()
        users_rows = curso.execute("SELECT * FROM users")
        admin_rows = curso.execute("SELECT * FROM admin")
        return render_template('pages/all_orders.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows, admin_rows= admin_rows)


@app.route('/users', methods=['GET', 'POST'])
@is_admin_logged_in
def users():
    curso = mysql.connection.cursor()
    if request.method == 'POST':
        query = request.form['search']
        standardlize ="%"+request.form['search']+"%"
        users_rows = curso.execute("SELECT * FROM users where username LIKE %s or mobile LIKE  %s",(standardlize,standardlize))
        result = curso.fetchall()
        flash('Search results for: {}'.format(query),'success')
        return render_template('pages/all_users.html', result=result, users_rows=users_rows)
    else:                       
        num_rows = curso.execute("SELECT * FROM products")
        order_rows = curso.execute("SELECT * FROM orders")
        users_rows = curso.execute("SELECT * FROM users")
        users_details = curso.fetchall()
        admin_rows = curso.execute("SELECT * FROM admin")
        
        return render_template('pages/all_users.html', users_details=users_details, row=num_rows, order_rows=order_rows,
                            users_rows=users_rows, admin_rows=admin_rows )
@app.route('/all_admin', methods=['GET', 'POST'])
@is_admin_logged_in
def all_admin():
    curso = mysql.connection.cursor()
    if request.method == 'POST':
        query = request.form['search']
        standardlize ="%"+request.form['search']+"%"
        users_rows = curso.execute("SELECT * FROM admin where email LIKE %s or mobile LIKE  %s",(standardlize,standardlize))
        result = curso.fetchall()
        flash('Search results for: {}'.format(query),'success')
        return render_template('pages/all_admin.html', result=result, users_rows=users_rows)
    else:                       
        num_rows = curso.execute("SELECT * FROM products")
        order_rows = curso.execute("SELECT * FROM orders")
        users_rows = curso.execute("SELECT * FROM users")
        admin_rows = curso.execute("SELECT * FROM admin")
        admin_details = curso.fetchall()
        
        return render_template('pages/all_admin.html',  row=num_rows, order_rows=order_rows,
                            users_rows=users_rows , admin_details = admin_details, admin_rows = admin_rows)


@app.route('/admin_add_product', methods=['POST', 'GET'])
@is_admin_logged_in
@is_manager
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form['price']
        description = request.form['description']
        available = request.form['available']
        category = request.form['category']
        item = request.form['item']
        code = request.form['code']
        file = request.files['picture']
        if name and price and description and available and category and item and code and file:
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")
            if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                save_photo = photos.save(file, folder=category)
                if save_photo:
                    # Create Cursor
                    curs = mysql.connection.cursor()
                    curs.execute("INSERT INTO products(pName,price,description,available,category,item,pCode,picture)"
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (name, price, description, available, category, item, code, picture))
                    mysql.connection.commit()
                    product_id = curs.lastrowid
                    curs.execute("INSERT INTO product_level(product_id)" "VALUES(%s)", [product_id])
                    if category == 'laptop':
                        level = request.form.getlist('laptop')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            mysql.connection.commit()
                    elif category == 'keyboard':
                        level = request.form.getlist('keyboard')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            mysql.connection.commit()
                    elif category == 'screen':
                        level = request.form.getlist('screen')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            mysql.connection.commit()
                    elif category == 'mouse':
                        level = request.form.getlist('mouse')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            mysql.connection.commit()
                    else:
                        flash('Không tìm thấy danh mục của sản phẩm', 'danger')
                        return redirect(url_for('admin_add_product'))
                    # Close Connection
                    curs.close()

                    flash('Thêm sản phẩm thành công', 'success')
                    return redirect(url_for('admin_add_product'))
                else:
                    flash('Ảnh chưa được lưu', 'danger')
                    return redirect(url_for('admin_add_product'))
            else:
                flash('Định dạng file không hỗ trợ', 'danger')
                return redirect(url_for('admin_add_product'))
        else:
            flash('Vui lòng điền đầy đủ thông tin', 'danger')
            return redirect(url_for('admin_add_product'))
    else:
        return render_template('pages/add_product.html')


@app.route('/edit_product', methods=['POST', 'GET'])
@is_admin_logged_in
@is_manager
def edit_product():
    if 'id' in request.args:
        product_id = request.args['id']
        curso = mysql.connection.cursor()
        res = curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        curso.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))
        product_level = curso.fetchall()
        if res:
            if request.method == 'POST':
                name = request.form.get('name')
                price = request.form['price']
                description = request.form['description']
                available = request.form['available']
                category = request.form['category']
                item = request.form['item']
                code = request.form['code']
                file = request.files['picture']
                # Create Cursor
                if name and price and description and available and category and item and code and file:
                    pic = file.filename
                    photo = pic.replace("'", "")
                    picture = photo.replace(" ", "")
                    if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file.filename = picture
                        save_photo = photos.save(file, folder=category)
                        if save_photo:
                            # Create Cursor
                            cur = mysql.connection.cursor()
                            exe = curso.execute(
                                "UPDATE products SET pName=%s, price=%s, description=%s, available=%s, category=%s, item=%s, pCode=%s, picture=%s WHERE id=%s",
                                (name, price, description, available, category, item, code, picture, product_id))
                            if exe:
                                if category == 'laptop':
                                    level = request.form.getlist('laptop')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'keyboard':
                                    level = request.form.getlist('keyboard')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'screen':
                                    level = request.form.getlist('screen')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                elif category == 'mouse':
                                    level = request.form.getlist('mouse')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        mysql.connection.commit()
                                else:
                                    flash('Không tìm thấy danh mục của sản phẩm', 'danger')
                                    return redirect(url_for('admin_add_product'))
                                flash('Sản phẩm được cập nhật', 'success')
                                return redirect(url_for('edit_product'))
                            else:
                                flash('Dữ liệu được cập nhật', 'success')
                                return redirect(url_for('edit_product'))
                        else:
                            flash('Chưa upload hình ảnh', 'danger')
                            return render_template('pages/edit_product.html', product=product,
                                                   product_level=product_level)
                    else:
                        flash('File không hỗ trợ', 'danger')
                        return render_template('pages/edit_product.html', product=product,
                                               product_level=product_level)
                else:
                    flash('Điền đầy đủ thông tin !!!', 'danger')
                    return render_template('pages/edit_product.html', product=product,
                                           product_level=product_level)
            else:
                return render_template('pages/edit_product.html', product=product, product_level=product_level)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin_add_employee', methods=['POST', 'GET'])
@is_admin_logged_in
@is_manager
def admin_add_employee():
    if request.method == 'POST':
        print(request.form)
        fullName = request.form['fullName']
        email = request.form['email']
        address = request.form['address']
        password = sha256_crypt.encrypt(str(request.form['password']))
        phone = request.form['phone']
        type = request.form['type']
     
        if fullName and email and address and password and phone and type:
            # Create Cursor
            curs = mysql.connection.cursor()
            curs.execute("INSERT INTO admin(fullName, email, mobile, address, password, type)"
                            "VALUES( %s, %s, %s, %s, %s, %s)",(fullName, email, phone, address, password, type))
            mysql.connection.commit()
    
            # Close Connection
            curs.close()

            flash('Thêm nhân viên thành công', 'success')
            return redirect(url_for('admin_add_employee'))
              
            
    else:
        return render_template('pages/add_employee.html')

@app.route('/edit_employee', methods=['POST', 'GET'])
@is_admin_logged_in
@is_manager
def edit_employee():
    if 'id' in request.args:
        user_id = request.args['id']
        print(user_id)
        curso = mysql.connection.cursor()
        res = curso.execute("SELECT * FROM admin WHERE id=%s", (user_id))
        user = curso.fetchall()
        curso.close()
        if res:
            if request.method == 'POST':
                fullName = request.form['fullName']
                email = request.form['email']
                address = request.form['address']
                password = sha256_crypt.encrypt(str(request.form['password']))
                phone = request.form['phone']
                type = request.form['type']
                # Create Cursor
                if fullName and email and address and password and phone and type:
                    cur = mysql.connection.cursor()
                    exe = cur.execute(
                        "UPDATE admin SET fullName=%s,email=%s,mobile=%s,address=%s,password=%s,type=%s where id = %s",
                        (fullName, email, phone, address, password, type,user_id) )
                    mysql.connection.commit()
    
                    # Close Connection
                    cur.close()
                    flash('Update user success', 'success')
                    return render_template('pages/edit_employee.html', user=user[0])
                else:
                    flash('Fill all field', 'danger')
                    return render_template('pages/edit_employee.html', user=user[0])
            else:
                return render_template('pages/edit_employee.html', user=user[0])
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/edit_user', methods=['POST', 'GET'])
@is_admin_logged_in
@is_manager
def edit_user():
    if 'id' in request.args:
        user_id = request.args['id']
        curso = mysql.connection.cursor()
        res = curso.execute(f"SELECT * FROM users WHERE id={user_id}")
        user = curso.fetchall()
        curso.close()
        if res:
            if request.method == 'POST':
                name = request.form['name']
                email = request.form['email']
                password = sha256_crypt.encrypt(str(request.form['password']))
                phone = request.form['mobile']
                username = request.form['username']
                role = request.form['role']
                # Create Cursor
                if name and email and password and phone and role and username:
                    cur = mysql.connection.cursor()
                    exe = cur.execute(f"UPDATE users SET name='{name}',email='{email}',username='{username}',password='{password}',mobile='{phone}',role='{role}' WHERE id = {user_id}")
                    mysql.connection.commit()
    
                    # Close Connection
                    cur.close()
                    flash('Update user success', 'success')
                    return render_template('pages/edit_user.html', user=user[0])
                else:
                    flash('Fill all field', 'danger')
                    return render_template('pages/edit_user.html', user=user[0])
            else:
                return render_template('pages/edit_user.html', user=user[0])
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))
@app.route('/delete_user', methods=['POST', 'GET'])
@is_admin_logged_in
@is_manager
def delete_user():
    if 'id' in request.args:
        user_id = request.args['id']
        curso = mysql.connection.cursor()
        res = curso.execute(f"SELECT * FROM users WHERE id={user_id}")
        user = curso.fetchall()
        curso.close()
        if res:
            if request.method == 'POST':
                    cur = mysql.connection.cursor()
                    exe = cur.execute(f"DELETE FROM users  WHERE id = {user_id}")
                    mysql.connection.commit()
    
                    # Close Connection
                    cur.close()
                    if exe:

                        flash('Delete product successfullys', 'success')
                        return redirect(url_for('admin_login'))
                    else:
                        flash('Delete product failed', 'danger')
                        return redirect(url_for('admin_login'))
            else:
                return render_template('pages/delete_user.html', user=user[0])
    else:
        return redirect(url_for('admin_login'))
@app.route('/delete_product', methods=['POST', 'GET'])
@is_admin_logged_in
@is_manager
def delete_product():
    if 'id' in request.args:
        user_id = request.args['id']
        curso = mysql.connection.cursor()
        res = curso.execute(f"SELECT * FROM products WHERE id={user_id}")
        user = curso.fetchall()
        curso.close()
        if res:
            if request.method == 'POST':
                    cur = mysql.connection.cursor()
                    exe = cur.execute(f"DELETE FROM products  WHERE id = {user_id}")

                    mysql.connection.commit()
    
                    # Close Connection
                    cur.close()
                    if exe:

                        flash('Delete product successfullys', 'success')
                        return redirect(url_for('admin_login'))
                    else:
                        flash('Delete product failed', 'danger')
                        return redirect(url_for('admin_login'))
            else:
                return render_template('pages/delete_product.html', user=user[0])
    else:
        return redirect(url_for('admin_login'))
@app.route('/delete_admin', methods=['POST', 'GET'])
@is_admin_logged_in
@is_manager
def delete_admin():
    if 'id' in request.args:
        user_id = request.args['id']
        curso = mysql.connection.cursor()
        res = curso.execute(f"SELECT * FROM admin WHERE id={user_id}")
        user = curso.fetchall()
        print(user[0])
        curso.close()
        if res:
            if request.method == 'POST':
                    cur = mysql.connection.cursor()
                    exe = cur.execute(f"DELETE FROM admin  WHERE id = {user_id}")
                    mysql.connection.commit()
    
                    # Close Connection
                    cur.close()
                    if exe:

                        flash('Delete product successfullys', 'success')
                        return redirect(url_for('admin_login'))
                    else:
                        flash('Delete product failed', 'danger')
                        return redirect(url_for('admin_login'))
            else:
                return render_template('pages/delete_admin.html', user=user[0])
    else:
        return redirect(url_for('admin_login'))
@app.route('/search', methods=['POST', 'GET'])
def search():
    form = OrderForm(request.form)
    if 'q' in request.args:
        q = request.args['q']
        # Create cursor
        cur = mysql.connection.cursor()
        # Get message
        query_string = "SELECT * FROM products WHERE pName LIKE %s ORDER BY id ASC"
        cur.execute(query_string, ('%' + q + '%',))
        products = cur.fetchall()
        # Close Connection
        cur.close()
        flash('Danh sách tìm kiếm sản phẩm: ' + q, 'success')
        return render_template('search.html', products=products, form=form)
    else:
        flash('Không tìm thấy sản phẩm', 'danger')
        return render_template('search.html')


@app.route('/profile')
@is_logged_in
def profile():
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                curso.execute("SELECT * FROM orders WHERE uid=%s ORDER BY id ASC", (session['uid'],))
                res = curso.fetchall()
                return render_template('profile.html', result=res)
            else:
                flash('Cần đăng nhập!', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Cần đăng nhập!', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Cần đăng nhập!', 'danger')
        return redirect(url_for('login'))


class UpdateRegisterForm(Form):
    name = StringField('Họ và tên', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Họ và tên'})
    email = EmailField('Email', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})
    mobile = StringField('Số điện thoại', [validators.length(min=10, max=15)], render_kw={'placeholder': 'Số điện thoại'})


@app.route('/settings', methods=['POST', 'GET'])
@is_logged_in
def settings():
    form = UpdateRegisterForm(request.form)
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                if request.method == 'POST' and form.validate():
                    name = form.name.data
                    email = form.email.data
                    password = sha256_crypt.encrypt(str(form.password.data))
                    mobile = form.mobile.data

                    # Create Cursor
                    cur = mysql.connection.cursor()
                    exe = cur.execute("UPDATE users SET name=%s, email=%s, password=%s, mobile=%s WHERE id=%s",
                                      (name, email, password, mobile, q))
                    if exe:
                        flash('Profile updated', 'success')
                        return render_template('user_settings.html', result=result, form=form)
                    else:
                        flash('Profile not updated', 'danger')
                return render_template('user_settings.html', result=result, form=form)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


class DeveloperForm(Form):  #
    id = StringField('', [validators.length(min=1)],
                     render_kw={'placeholder': 'Nhập id sản phẩm'})


@app.route('/developer', methods=['POST', 'GET'])
def developer():
    form = DeveloperForm(request.form)
    if request.method == 'POST' and form.validate():
        q = form.id.data
        curso = mysql.connection.cursor()
        result = curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        if result > 0:
            x = content_based_filtering(q)
            wrappered = wrappers(content_based_filtering, q)
            execution_time = timeit.timeit(wrappered, number=0)
            seconds = ((execution_time / 1000) % 60)
            return render_template('developer.html', form=form, x=x, execution_time=seconds)
        else:
            nothing = 'Nothing found'
            return render_template('developer.html', form=form, nothing=nothing)
    else:
        return render_template('developer.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
