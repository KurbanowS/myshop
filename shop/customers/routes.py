from flask import render_template, redirect, request, url_for, flash, session, current_app
from shop import db, app, photos
from .forms import CustomerRegisterForm
import secrets, os

@app.route('/customer/register')
def customer_register():
    return render_template('customer/register.html', title="Register")