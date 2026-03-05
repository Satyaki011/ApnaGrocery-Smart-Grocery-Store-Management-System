from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Admin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint("auth", __name__)


@auth.route("/")
def home():
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password required.")
            return render_template("register.html")

        if Admin.query.filter_by(username=username).first():
            flash("Username already taken.")
            return render_template("register.html")

        admin = Admin(username=username, password=generate_password_hash(password))
        db.session.add(admin)
        db.session.commit()
        flash("Registration successful — please log in.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = Admin.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("auth.dashboard"))

        flash("Invalid credentials.")

    return render_template("login.html")


@auth.route("/dashboard")
@login_required
def dashboard():
    from models import Product, Supplier, Sale
    from sqlalchemy import func
    from datetime import datetime, timedelta
    from services.ai_service import ai_assistant

    total_products = Product.query.count()
    total_suppliers = Supplier.query.count()
    total_sales = Sale.query.count()

    # Calculate actual inventory value
    inventory_value = db.session.query(func.sum(Product.price * Product.quantity)).scalar() or 0

    # Get low stock items count (quantity <= 10)
    low_stock_count = Product.query.filter(Product.quantity <= 10).count()

    # Get today's revenue
    today = datetime.now().date()
    today_sales = Sale.query.filter(func.date(Sale.created_at) == today).all()
    today_revenue = sum(sale.quantity * (sale.product.price if sale.product else 0) for sale in today_sales)

    # Get expiring products (products with low quantity that might expire soon - arbitrary threshold)
    expiring_count = Product.query.filter(Product.quantity <= 5).count()

    # Get top selling products based on actual sales
    top_products = db.session.query(
        Product.name,
        func.sum(Sale.quantity).label('total_sold')
    ).join(Sale, Product.id == Sale.product_id
    ).group_by(Product.id, Product.name
    ).order_by(func.sum(Sale.quantity).desc()
    ).limit(5).all()

    # Get recent sales
    recent_sales = Sale.query.order_by(Sale.created_at.desc()).limit(10).all()

    # Get sales trend for last 7 days
    sales_trend = []
    labels = []
    for i in range(6, -1, -1):
        day = datetime.now().date() - timedelta(days=i)
        day_sales = Sale.query.filter(func.date(Sale.created_at) == day).all()
        revenue = sum(sale.quantity * (sale.product.price if sale.product else 0) for sale in day_sales)
        labels.append(day.strftime('%a'))
        sales_trend.append(revenue)

    # Get stock distribution
    in_stock = Product.query.filter(Product.quantity > 50).count()
    low_stock = Product.query.filter(Product.quantity > 0, Product.quantity <= 50).count()
    out_of_stock = Product.query.filter(Product.quantity == 0).count()

    # Get alerts (low stock products)
    low_stock_products = Product.query.filter(Product.quantity <= 10).all()
    alerts = []
    for p in low_stock_products:
        alerts.append({
            'title': f'Low Stock: {p.name}',
            'message': f'Only {p.quantity} units remaining',
            'level': 'Warning'
        })

    # Get AI Insights
    ai_insights = ai_assistant.get_auto_insights()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_suppliers=total_suppliers,
        total_sales=total_sales,
        inventory_value=inventory_value,
        low_stock_count=low_stock_count,
        today_revenue=today_revenue,
        expiring_count=expiring_count,
        top_products=top_products,
        recent_sales=recent_sales,
        sales_trend=sales_trend,
        sales_labels=labels,
        stock_distribution=[in_stock, low_stock, out_of_stock],
        alerts=alerts,
        ai_insights=ai_insights,
    )


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))