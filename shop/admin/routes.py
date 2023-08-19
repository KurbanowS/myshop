from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Addproduct, Brand, Category
import os


@app.route('/admin')
def home():
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title ='Admin page', products=products)


@app.route('/brands')
def brands():
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='Brand page', brands=brands)


@app.route('/categories')
def categories():
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='Category page', categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name = form.name.data, username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(user)
        flash(f'Welcome {form.name.data}. Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title = 'Registration page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if user:
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data}, You are logedin', 'success')
            return redirect(url_for('home'))
        else:
            flash('Wrong password or username please try again', 'danger')
            return redirect(url_for('login'))
    return render_template('admin/login.html', form=form, title='Login page')
        

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))