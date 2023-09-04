from flask import *
from database import *
from funcs import *
import jwt
import datetime 
import os
from flask_cors import CORS 
from flask_bcrypt import Bcrypt

app = Flask(__name__)  # '__main__' 
Bcrypt(app)
CORS(app, support_credentials=True)


# The HomePage
@app.route('/')
def home_template():
    return render_template('home.html')
# The cart section
@app.route('/cart')
def cart_template():
    return render_template('cart.html')
# The payment section
@app.route('/checkout')
def checkout_template():
    return render_template('checkout.html')
# Order section for customers making order
@app.route('/order')
# @token_required
def order_template():
    return render_template('order.html')
# Login and Sign up Page
@app.route('/login', methods=['GET','POST'])
def login_template():
    if request.method == 'POST':
        data = request.form
        if login_user(data) == data['email']:
            user = data['email']
            token = jwt.encode({'user': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, os.getenv('SECRET_KEY'))
            return set_cookies(token)
        elif login_user(data) == 'admin':
            user = 'admin'
            token = jwt.encode({'user': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, os.getenv('SECRET_KEY'))
            return set_cookies(token)
        return  render_template('login.html', message="Email Or Password Incorrect")
    else:
        return render_template('login.html')   
# ---------------------------------------- 
@app.route('/register', methods=['POST'])
def reg_template():
    data = request.form
    registration(data) 
    return render_template('login.html', reg_message="Registered Successfully!")
# Contact of the Website
@app.route('/contact')
def contact_template():
    return render_template('contact-us.html')
# Questions and Answers for Product usage
@app.route('/faqs')
def faq_template(): 
    return render_template('faq.html')
# To display  a list of vendors
# @app.route('/vendors-list')
# def vendorslist_template():
#     return render_template('vendor-dokan-store-list.html')
# Your like items on the catalog
@app.route('/favourite')
def favourite_template():
    return render_template('wishlist.html')
# The list of vendors in grid style
# @app.route('/vendors-grid')
# def vendorsgrid_template():
#     return render_template('vendor-dokan-store-grid.html')
# Comparison of different products on the store of a vendor
@app.route('/compare-products')
def compare_template():
    return render_template('compare.html')
#  The about us page
@app.route('/about')
def about_template():
    return render_template('about-us.html')
# Your account login of the seller or vendor
@app.route('/account')
@token_required
def account_template():
    active_user = user_account()['user'] 
    return render_template('my-account.html', username=active_user)
# A singlr post description of a blog
@app.route('/post')
def post_template():
    return render_template('post-single.html')
# This is the viewing of oreder for the vendor to see all the items he has sold 
@app.route('/orderView')
def orderView_template():
    return render_template('order-view.html')
# This is the complete list of all the items in the catalog of the website
@app.route('/catalog')
def catalog_template():
    products = get_products()
    return render_template('shop-horizontal-filter.html', products=products)
# The signup page for anyone that wants to become a vendor
# @app.route('/vendors-sign')
# def vendorSign_template():
#     return render_template('become-a-vendor.html')
# The ovverview of a particular product
@app.route('/product/<int:id>')
def product_template(id):  
    product = get_product(id)  
    # Length of products for More-products to display three
    products = more_products() 
    # -----------------------------------------------------
    print(products)
    similar_products = product_by_category(get_product(id).category)  
    return render_template('product-variable.html', pid=id, product=product, more_products=products, related_products=similar_products)
# a single vendor overview
# @app.route('/vendor')
# def vendor_template():
#     return render_template('vendor-dokan-store.html')
# For account settings on user dashboard
@app.route('/account_settings', methods=['POST']) 
def account_details():
    data = request.form
    return save_user_settings(data)
# For User's account password
@app.route('/account_password', methods=['POST']) 
def account_password():
    data = request.form
    
    if data['new_password'] != data['conf_password']:
        return render_template('my-account.html', pass_message="Passwords Doesn't Match")
    return update_user_password(data)
# Logout user from session
@app.route('/logout')
def logout_user():
    return del_cookies()
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
      
      
##############################################################################################################    
##############################################################################################################  
    #   THE ADMIN PANEL AND ROUTES HANDLING FOR THIS ECOMMERCE PLATFORM/WEBSITE   #
##############################################################################################################
##############################################################################################################
#  The dashboard of the admin
@app.route('/admin/dashboard')
@token_required
@check_ifadmin
def admin_dashboard():
    products = product_total() # Total Products Listed
    customers_Total = customers_total() # Total customers registered
    return render_template('/admin/index.html', products=products, customers=customers_Total)
# Admin adding a new product
@app.route('/admin/create-product', methods=['POST','GET'])
@token_required
@check_ifadmin
def new_product():
    if request.method  == 'POST':
        data = request.form 
        new_product = create_new_product(data)  
        if new_product == True:
            return render_template('/admin/product-create.html', new_product="Sucessfully created new product")
        return  render_template('/admin/product-create.html', new_product=" new product not created, try again!")
    else:
        return render_template('/admin/product-create.html')
# The products lists in admin panel
@app.route('/admin/products') 
@token_required
@check_ifadmin
def products_admin(): 
    total = product_total()
    # get the array of the products from database
    products = get_products()
    return render_template('/admin/product-list.html', products=products, total=total)
# This is the route for Checking Orders Made
@app.route('/admin/orders')
@token_required
@check_ifadmin
def orders_made():
    return render_template('/admin/orders-list-view.html') 
# This is the route for knowing how many users are active or not annd in total in the platform
@app.route('/admin/users')
@token_required
@check_ifadmin
def users():
    return render_template('/admin/users-list.html')
#This is the route for all TRANSACTIONS
@app.route('/admin/transactions') 
def transactions():
    return render_template('/admin/transactions.html')
# This is the reviews page Customers/Users have written
@app.route('/admin/reviews')
@token_required
@check_ifadmin
def reviews():
    return render_template('/admin/reviews-ratings.html')
# This is the route for the shipments of a product 
@app.route('/admin/shipments')
@token_required
@check_ifadmin
def shipments():
    return render_template('/admin/shipments.html')



# For running the app
if __name__ == '__main__':
    app.run(debug=True)