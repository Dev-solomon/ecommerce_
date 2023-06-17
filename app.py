from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)  # '__main__'
app.secret_key = "solomon"

@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/cart')
def cart_template():
    return render_template('cart.html')

@app.route('/checkout')
def checkout_template():
    return render_template('checkout.html')

@app.route('/')
def home_template():
    return render_template('home.html')

# For running the app
if __name__ == '__main__':
    app.run(debug=True)