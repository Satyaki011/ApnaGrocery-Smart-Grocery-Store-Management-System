from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Sale, Product

sales = Blueprint("sales", __name__)

@sales.route("/sales", methods=["GET", "POST"])
def list_sales():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        quantity   = request.form.get("quantity", 0)

        if product_id and quantity:
            try:
                product = Product.query.get(int(product_id))

                if not product:
                    flash("Product not found.", "danger")
                elif int(quantity) > product.quantity:
                    flash(f"Not enough stock! Available: {product.quantity}", "warning")
                else:
                    # Stock ghataao
                    product.quantity -= int(quantity)

                    new_sale = Sale(
                        product_id=int(product_id),
                        quantity=int(quantity)
                    )
                    db.session.add(new_sale)
                    db.session.commit()
                    flash("Sale recorded successfully!", "success")

            except Exception as e:
                db.session.rollback()
                flash(f"Error: {str(e)}", "danger")
        else:
            flash("Please select product and quantity.", "warning")

        return redirect(url_for("sales.list_sales"))

    # GET
    try:
        items    = Sale.query.order_by(Sale.created_at.desc()).all()
        products = Product.query.filter(Product.quantity > 0).all()
    except Exception:
        items    = []
        products = []

    return render_template("sales.html", sales=items, products=products)