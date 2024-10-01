from flask import Blueprint, render_template, flash,redirect,request,jsonify
from .forms import SignUpForm, LogInForm
from .models import Product,Cart,Order
from . import db
from flask_login import login_user, login_required, logout_user, current_user

view = Blueprint('view', __name__)


@view.route('/')
def home():
    items = Product.query.filter_by(flash_sale=True)
    if items:
        return render_template('home.html', items=items)

    return render_template('home.html')


@view.route('/product-view/<int:item_id>')
def open_item(item_id):
    item = Product.query.get(item_id)
    return render_template('product_view.html', item=item)



from flask import jsonify

@view.route('/add-cart', methods=['POST'])
@login_required
def add_to_cart():
    # Get JSON object
    data = request.get_json()
    item_id = data.get('id')
    if not item_id:
        return jsonify({'error': 'Invalid item ID'}), 400

    print(f'The item ID: {item_id}')

    # Get the current user's cart item for the product
    check_cart = Cart.query.filter_by(customer_link=current_user.id, product_link=item_id).first()

    if check_cart:
        # Product exists in the cart, increase quantity
        check_cart.quantity += 1
        cart = check_cart
    else:
        # Product does not exist in the cart, create new cart entry
        cart = Cart(customer_link=current_user.id, product_link=item_id, quantity=1)

    # Add or update in the database
    try:
        # Add cart to the session only if it's a new entry
        if not check_cart:
            db.session.add(cart)
        db.session.commit()
        # making function
    except Exception as e:
        db.session.rollback()  # Rollback if an error occurs
        print(e)  # For debugging
        flash('Item was not added to the cart')



@view.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    total_price = 0
    # sending the cart
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    if cart:
        for item in cart:
            total_price += item.product.current_price * item.quantity
    print(f"total price: {total_price}")

    return render_template('cart.html', cart=cart, total_price=total_price)


@view.route('/delete-item/<int:item_id>')
def delete_item_cart(item_id):
    item = Cart.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect('/cart')


# update quantity from the cart
@view.route('/update-quantity', methods=['POST'])
def update_quantity():
    # Get the JSON object from the request
    data = request.get_json()
    item_id = data.get('id')
    action = data.get('action')

    # Query the cart item by its id
    cart_item = Cart.query.get(item_id)

    if cart_item:
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease":
            if cart_item.quantity > 1:  # Prevent quantity from going below 1
                cart_item.quantity -= 1
            else:
                return jsonify({"error": "Quantity cannot be less than 1"}), 400
        else:
            return jsonify({"error": "Invalid action"}), 400

        # Commit the changes to the database
        db.session.commit()

        total_price = 0
        # Querying all cart items for the current user
        cart_items = Cart.query.filter_by(customer_link=current_user.id).all()
        if cart_items:
            for item in cart_items:
                total_price += item.product.current_price * item.quantity

        # Fixed shipping cost
        shipping_cost = 20

        # Total with shipping
        total_with_shipping = shipping_cost + total_price

        # Get the updated quantity from the modified cart item
        new_quantity = cart_item.quantity
        return jsonify({
            "quantity": new_quantity,
            "total_price": total_price,
            "shipping_cost": shipping_cost,
            "total_with_shipping": total_with_shipping
        }), 200

    else:
        # Handle the case where the item does not exist
        print('Item does not exist')
        return jsonify({"error": "Product not found"}), 404



@view.route('/order', methods=['POST', 'GET'])
def order():
    # Get the items from the cart that belong to the customer
    user_cart = Cart.query.filter_by(customer_link=current_user.id).all()

    if user_cart:
        total_price = 0
        for item in user_cart:
            total_price += item.quantity * item.product.current_price

            # Create a new order for each item
            new_order = Order(
                quantity=item.quantity,
                price=item.product.current_price,
                status='pending',
                customer_link=item.customer_link,
                product_link=item.product_link
            )

            try:
                db.session.add(new_order)

                # Reduce product stock
                if item.product.in_stock > 0:
                    item.product.in_stock -= item.quantity

                # Delete the item from the cart
                db.session.delete(item)
                print(f'item is deleted {item}')

                db.session.commit()


            except Exception as e:
                db.session.rollback()
                print(str(e))

    orders = Order.query.filter_by(customer_link = current_user.id).all() or[]
    return render_template('order.html',orders=orders)
