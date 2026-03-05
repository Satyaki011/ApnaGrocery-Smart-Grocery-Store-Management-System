from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Product

products = Blueprint("products", __name__)


@products.route("/products", methods=["GET", "POST"])
def list_products():
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        price    = request.form.get("price", 0)
        quantity = request.form.get("quantity", 0)

        if name:
            try:
                new_product = Product(
                    name=name,
                    price=float(price),
                    quantity=int(quantity)
                )
                db.session.add(new_product)
                db.session.commit()
                flash("Product added successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error adding product: {str(e)}", "danger")
        else:
            flash("Product name is required.", "warning")

        return redirect(url_for("products.list_products"))

    # GET
    try:
        items = Product.query.all()
    except Exception:
        items = []

    return render_template("products.html", products=items)