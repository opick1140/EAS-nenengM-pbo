from flask import Flask, render_template, request, redirect, url_for, session, json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load data produk dari file JSON
def load_products():
    with open('products.json', 'r') as file:
        return json.load(file)

@app.route('/')
def home():
    products = load_products()
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    products = load_products()
    cart_items = {int(k): v for k, v in session.get('cart', {}).items()}
    total = sum(products[p-1]['price'] * q for p, q in cart_items.items())
    return render_template('cart.html', cart=cart_items, products=products, total=total)

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)
