from shop import app, db
from shop.products.models import Addproduct, Category, Brand
from shop.customers.models import Register, CustomerOrder
from shop.admin.models import User

@app.shell_context_processor
def make_shell_processor():
    return {'db':db, 'Addproduct':Addproduct, 'Category':Category, 'Brand':Brand, 'Register': Register, 'CustomerOrder':CustomerOrder, 'User': User}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')