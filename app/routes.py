# file with all endpoints
import time
from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddProductToCart, EditProfileForm, ChangePassword, NewPassword
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Product, Order, Products_for_order
from werkzeug.urls import url_parse
from app.email import send_email, send_password_reset_email


def sum_order():
    if 'card' in session:
        price_total = sum([list_item['price'] for list_item in session['card']])
        quantity_total = sum([list_item['quantity'] for list_item in session['card']])
        return price_total, quantity_total
    else:
        return 0,0


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html', title='FRIDAYS')


@app.route('/index', methods=['GET', 'POST'])
def index():
    # for menu
    products = Product.query.all()
    product_group = Product.query.with_entities(Product.product_type).distinct()
    form = AddProductToCart()
    # product id list
    if form.is_submitted():
        # active button
        if 'card' in session:
            session_id = []
            for list_item in session['card']:
                if list_item['id'] not in session_id:
                    session_id.append(list_item['id'])
            if form.code.data in session_id:
                for list_item in session['card']:
                    if list_item['id'] == form.code.data:
                        list_item['quantity'] += 1
                        list_item['price'] = list_item['quantity'] * form.price.data
            else:
                session['card'].append({'id': form.code.data, 'name': form.name.data, 'quantity': 1,
                                        'price': form.price.data})
            session.modified = True
    price_total, quantity_total = sum_order()
    return render_template('index.html', title='Menu', products=products, len=len(products),
                           product_group=product_group, form=form,
                           price_total=price_total, quantity_total=quantity_total)


@app.route('/make_order', methods=['GET', 'POST'])
def make_order():
    price_total, quantity_total = sum_order()

    if request.method == 'POST':
        if current_user.is_authenticated:
            order = Order(user_id=current_user.id)
            if 'card' in session:
                for item in session['card']:
                    product = Products_for_order(product_id=item['id'], quantity=item['quantity'],
                                                 total_price=item['price'], order_id=order.order_id)
                    if product.quantity == 0:
                        continue
                    else:
                        order.items.append(product)
        else:
            return redirect(url_for('login'))

        db.session.add(order)
        db.session.commit()
        flash('You make an order', 'make_order')
        send_email('[Fridays] New order',
                   sender='admin@fridays.com',
                   recipients=[current_user.email],
                   text_body=render_template('email/new_order.txt', user=current_user),
                   html_body=render_template('email/new_order.html', user=current_user))

        session['card'] = []
        quantity_total = 0
        price_total = 0

    return render_template('cart.html', title='Cart', products_in_order=session['card'], price_total=price_total,
                           quantity_total=quantity_total)


@app.route('/delete_item/<int:id>')
def delete_item(id):
    referrer = request.referrer
    session.modified = True
    for index, list_item in enumerate(session['card']):
        for key, value in list_item.items():
            if list_item[key] == id:
                session['card'].pop(index)
                if referrer == 'http://127.0.0.1:5000/make_order':
                    return redirect(url_for('make_order'))
                else:
                    return redirect(url_for('index'))


@app.route('/minus_quantity/<int:id>')
def minus_quantity(id):
    session.modified = True
    for index, list_item in enumerate(session['card']):
        for key, value in list_item.items():
            if list_item[key] == id:
                try:
                    if list_item['quantity'] > 1:
                        price_for_one = list_item['price'] / list_item['quantity']
                        list_item['quantity'] -= 1
                        list_item['price'] -= price_for_one
                        return redirect(url_for('make_order'))
                    else:
                        raise ZeroDivisionError
                except ZeroDivisionError:
                    session['card'].pop(index)
                    return redirect(url_for('make_order'))


@app.route('/plus_quantity/<int:id>')
def plus_quantity(id):
    session.modified = True
    for index, list_item in enumerate(session['card']):
        for key, value in list_item.items():
            if list_item[key] == id:
                price_for_one = list_item['price'] / list_item['quantity']
                list_item['quantity'] += 1
                list_item['price'] += price_for_one
                return redirect(url_for('make_order'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'login')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, phone_number=form.phone_number.data)
        user.set_password(form.password.data)
        db.session.add(user)
        flash('Congratulations, you are now a registered user!', 'register')
        time.sleep(5)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', title='Profile', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/check_data', methods=['GET', 'POST'])
def check_data():
    form = ChangePassword()
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password.", 'check_data')
    else:
        flash('This email is not in the database', 'check_data')
    return render_template('change_pswrd.html', title='Reset Password', form=form)


@app.route('/change_pswd/<token>', methods=['GET', 'POST'])
def change_pswd(token):
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = NewPassword()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'change_pswd')
        return redirect(url_for('login'))
    return render_template('new_pswd.html', form=form)
