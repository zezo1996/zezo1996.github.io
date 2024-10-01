from flask import Blueprint, render_template, flash,redirect,send_from_directory,request,url_for,jsonify
from .forms import AddItems, Status
from .models import Product,Cart,Order,Customer
from . import db
from flask_login import login_user, login_required, logout_user,current_user
from werkzeug.utils import secure_filename
admin = Blueprint('admin', __name__)

@admin.route('/add-items', methods=['POST', 'GET'])
def add_items():
    form = AddItems()
    # print(f'this is the user id:{current_user.id}')

    if form.validate_on_submit():
        product_name = form.product_name.data
        current_price = form.current_price.data
        previous_price = form.previous_price.data
        in_stock = form.in_stock.data
        flash_sale = form.flash_sale.data

        # Handling picture upload
        file = form.product_picture.data
        if file:
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            try:
                file.save(file_path)
            except Exception as e:
                flash(f"Error saving the file: {e}", "error")
                return render_template('add_items.html', form=form)

        # Creating a new Product instance
        new_item = Product(
            product_name=product_name,
            current_price=current_price,
            previous_price=previous_price,
            in_stock=in_stock,
            flash_sale=flash_sale,
            product_picture=file_path,
            admin_link=current_user.id
        )

        try:
            db.session.add(new_item)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect('/add-items')
        except Exception as e:
            db.session.rollback()  # Roll back the transaction if an error occurs
            flash(f"Error adding the product: {e}", "error")

    return render_template('add_items.html', form=form)


# making a route to serve the img that coming from another dierctory
@admin.route('/media/<path:filename>')
def get_img(filename):
    return send_from_directory('../media',filename)


@admin.route('/admin-items', methods=['GET', 'POST'])
def admin_items():
    # Get the list of products belonging to the current admin user
    items = Product.query.filter_by(admin_link=current_user.id).all() or []

    if request.method == 'POST':
        item_id = request.form.get('delete')

        # Check if item_id was provided in the form submission
        if item_id:
            try:
                # Fetch the product by ID
                item = Product.query.get(item_id)

                if item:
                    # Delete the product if found
                    db.session.delete(item)
                    db.session.commit()
                    flash('Product is deleted successfully', 'success')
                    return redirect('/admin-items')
                else:
                    flash('Product not found', 'warning')

            except Exception as e:
                print(f"Problem deleting the product from the table: {e}")
                flash('Product could not be deleted', 'danger')
    # Render the template with the list of items
    return render_template('admin_items.html', items=items)



from flask import render_template, redirect, flash
from werkzeug.utils import secure_filename
from flask_login import current_user

@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    # Fetch item by item_id
    item = Product.query.get(item_id)
    if item is None:
        flash('Item not found!', 'error')
        return redirect('/admin-items')
    # obj=item, Flask-WTF automatically populates the form fields with the data from the item object.
    form = AddItems(obj=item)  # Initialize form with item data

    if form.validate_on_submit():
        product_name = form.product_name.data
        current_price = form.current_price.data
        previous_price = form.previous_price.data
        in_stock = form.in_stock.data
        flash_sale = form.flash_sale.data

        # Handling picture upload
        file = form.product_picture.data
        if file:
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            try:
                file.save(file_path)
            except Exception as e:
                flash(f"Error saving the file: {e}", "error")
                return render_template('update_item.html', form=form)

        # Update item details
        try:
            item.product_name = product_name
            item.current_price = current_price
            item.previous_price = previous_price
            item.in_stock = in_stock
            item.flash_sale = flash_sale
            if file:
                item.product_picture = file_path
            item.admin_link = current_user.id
            db.session.commit()  # Commit the changes
            flash('Product has been updated successfully!', 'success')
            return redirect('/admin-items')
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'Product Not Updated: {e}', 'error')

    return render_template('update_item.html', form=form)



@admin.route('/sold-items', methods=['POST', 'GET'])
def sold_items():
    # Handle POST request to update order status
    if request.method == 'POST':
        # Get JSON object
        data = request.get_json()
        item_id = data.get('id')
        item_value = data.get('value')
        print(f'item_id {item_id} and value: {item_value}')


        if item_id and item_value:
            admin_order = Order.query.filter_by(id=item_id).first()

            if admin_order:  # Check if the order exists
                try:
                    admin_order.status = item_value
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()  # Rollback the session on error
                    print(e)

    # Retrieve orders related to the current admin's products and their corresponding customers
    orders = (
        db.session.query(Order)
        .join(Product)
        .join(Customer)
        .filter(Product.admin_link == current_user.id)
        .all()
    )

    # Prepare a list of dictionaries to store order and customer information
    order_details = [
        {
            'order_id': order.id,
            'quantity': order.quantity,
            'price': order.price,
            'status': order.status,
            'customer_email': order.customer.email,
            'customer_username': order.customer.username,
            'product_name': order.product.product_name,
            'product_picture': order.product.product_picture,
        }
        for order in orders
    ]

    # Return the rendered template for GET request
    return render_template('sold-items.html', orders=order_details)
