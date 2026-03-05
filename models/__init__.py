from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db
import pytz

KOLKATA = pytz.timezone("Asia/Kolkata")


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="ADMIN")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer, default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)


class Supplier(db.Model):
    __tablename__ = "suppliers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    item_name = db.Column(db.String(200), nullable=True)       # ✅ naya
    purchase_price = db.Column(db.Float, nullable=True)        # ✅ naya

class Sale(db.Model):
    __tablename__ = "sales"
    id         = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity   = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(KOLKATA))
    # ✅ Relationship add karo
    product    = db.relationship("Product", backref="sales")

# Simple alias for code that referenced 'Admin' as user model
User = Admin
