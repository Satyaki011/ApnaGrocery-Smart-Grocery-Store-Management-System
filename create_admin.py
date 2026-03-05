from app import app
from models import db, Admin
import os

username = os.environ.get("ADMIN_USER", "admin")
password = os.environ.get("ADMIN_PASS", "changeme")

with app.app_context():
    existing = Admin.query.filter_by(username=username).first()
    if existing:
        print(f"Admin already exists: {existing.id} {existing.username}")
    else:
        admin = Admin(username=username)
        admin.set_password(password)
        admin.role = os.environ.get("ADMIN_ROLE", "ADMIN")
        db.session.add(admin)
        db.session.commit()
        print(f"Created admin: username={username} password={password} role={admin.role}")
