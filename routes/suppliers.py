from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Supplier

suppliers = Blueprint("suppliers", __name__)

@suppliers.route("/suppliers", methods=["GET", "POST"])
def list_suppliers():
    if request.method == "POST":
        name           = request.form.get("name", "").strip()
        contact        = request.form.get("contact", "").strip()
        item_name      = request.form.get("item_name", "").strip()
        purchase_price = request.form.get("purchase_price", 0)

        if name:
            try:
                new_supplier = Supplier(
                    name=name,
                    contact=contact,
                    item_name=item_name,
                    purchase_price=float(purchase_price)
                )
                db.session.add(new_supplier)
                db.session.commit()
                flash("Supplier added successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error: {str(e)}", "danger")
        else:
            flash("Supplier name is required.", "warning")

        return redirect(url_for("suppliers.list_suppliers"))

    try:
        items = Supplier.query.all()
    except Exception:
        items = []

    return render_template("suppliers.html", suppliers=items)