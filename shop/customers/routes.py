from flask import render_template, redirect, request, url_for, flash, session, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, photos, login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Register, CustomerOrder
import secrets, os


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        user = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=form.password.data, country=form.country.data,
                        city=form.city.data, contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data, )
        db.session.add(user)
        flash(f'Welcome {form.username.data}. Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customer/register.html', title="Register", form=form)


@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user:
            login_user(user)
            flash('You are logedin!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect email or password','danger')
            return redirect(url_for('customerLogin'))
    return render_template('customer/login.html', title="Login", form=form)



@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('customerLogin'))


@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash('Something went wrong while get order', 'danger')
            return redirect(url_for('GetCart'))
        

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        subtotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).first()
        for _key, product in orders.orders.items():
            discount = (product['discount'] / 100) * float(product['price'])
            subtotal = float(product['price']) * int(product['quantity'])
            subtotal -= discount * int(product['quantity'])
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', title='Order place')
















