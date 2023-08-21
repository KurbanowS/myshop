from flask import render_template, redirect, request, url_for, flash, session, current_app
from shop import db, app, photos
from .forms import Addproducts
from .models import Category, Brand, Addproduct
import secrets, os


def barnds():
    barnds = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return barnds


def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', title="Home page", products=products, barnds=barnds(), categories=categories())


@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html', product=product, barnds=barnds(), categories=categories())


@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand = get_b).paginate(page=page, per_page=8)
    return render_template('products/index.html', title="Brand page", brand=brand, barnds=barnds(), categories=categories(), get_b=get_b)


@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category = get_cat).paginate(page=page, per_page=8)
    return render_template('products/index.html', title="Category page", get_cat_prod=get_cat_prod, barnds=barnds(), categories=categories(), get_cat=get_cat)


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash (f"The Brand {getbrand} was added", 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html',brands='brands', title = 'Add brand')


@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash('Your brand have succesfully updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update brand page', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    deletebrand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(deletebrand)
        flash(f'Brand {deletebrand.name} has been succesfully deleted', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    flash(f'Brand {deletebrand.name} can\'t be deleted', 'warning')


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    if request.method == 'POST':
        getcategory = request.form.get('category')
        cat = Category(name=getcategory)
        db.session.add(cat)
        flash (f"The Category {getcategory} was added", 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html', title = 'Add category')


@app.route('/updatecategory/<int:id>', methods=['GET','POST'])
def updatecategory(id):
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecategory.name = category
        flash('Your category have succesfully updated', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html', title='Update category page', updatecategory=updatecategory)


@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    deletecategory = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(deletecategory)
        flash(f'Category {deletecategory.name} has been succesfully deleted', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    flash(f'Category {deletecategory.name} can\'t be deleted', 'warning')


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method =="POST" and 'image_1' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'))
        image_2 = photos.save(request.files.get('image_2'))
        image_3 = photos.save(request.files.get('image_3'))
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, colors=colors, description=description, brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f"The product {name} has been added to your database", "success")
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('products/addproduct.html', title='Add product', form=form, brands=brands, categories=categories)


@app.route('/updateproduct/<int:id>', methods = ['GET','POST'])
def updateproduct(id):
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.description = form.description.data
        if request.files.get('image_1'):
            try:    
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'))
            except:
                product.image_1 = photos.save(request.files.get('image_1'))
        if request.files.get('image_2'):
            try:    
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'))
            except:
                product.image_2 = photos.save(request.files.get('image_2'))
        if request.files.get('image_3'):
            try:    
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'))
            except:
                product.image_3 = photos.save(request.files.get('image_3'))        
        flash('Your product has been updated', 'success')
        db.session.commit()
        return redirect(url_for('home'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.description
    brand = product.brand.name
    category = product.category.name
    return render_template('products/updateproduct.html', title='Update product', form=form, brands=brands, categories=categories, product=product)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    deleteproduct = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        try:    
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + deleteproduct.image_1))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + deleteproduct.image_2))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + deleteproduct.image_3))
        except Exception as e:
            print(e) 
        db.session.delete(deleteproduct)
        flash(f'Product {deleteproduct.name} has been successfully deleted', 'success')
        db.session.commit()
        return redirect(url_for('home'))
    flash(f'Product {deleteproduct.name} can\'t be deleted', 'danger')
    return redirect(url_for('home'))