from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)  # '__main__'
app.secret_key = "solomon"

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
def order_template():
    return render_template('order.html')
# Login and Sign up Page
@app.route('/login')
def login_template():
    return render_template('login.html')
# Contact of the Website
@app.route('/contact')
def contact_template():
    return render_template('contact-us.html')
# Questions and Answers for Product usage
@app.route('/faq')
def faq_template():
    return render_template('faq.html')
# To display  a list of vendors
@app.route('/vendors-list')
def vendorslist_template():
    return render_template('vendor-dokan-store-list.html')
# Your like items on the catalog
@app.route('/favourite')
def favourite_template():
    return render_template('wishlist.html')
# The list of vendors in grid style
@app.route('/vendors-grid')
def vendorsgrid_template():
    return render_template('vendor-dokan-store-grid.html')
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
def account_template():
    return render_template('my-account.html')
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
    return render_template('shop-horizontal-filter.html')
# The signup page for anyone that wants to become a vendor
@app.route('/vendors-sign')
def vendorSign_template():
    return render_template('become-a-vendor.html')
# The ovverview of a particular product
@app.route('/product')
def product_template():
    return render_template('product-variable.html')
# a single vendor overview
@app.route('/vendor')
def vendor_template():
    return render_template('vendor-dokan-store.html')




# For running the app
if __name__ == '__main__':
    app.run(debug=True)