from flask import Flask
from config import Config
from extensions import db, login_manager
from routes.auth import auth
from routes.products import products
from routes.suppliers import suppliers
from routes.sales import sales
from routes.ai import ai  # AI Assistant
from models import Admin


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # ✅ Login view set karo
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # ✅ 403 error fix — unauthorized users ko login page pe bhejo
    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import redirect, url_for
        return redirect(url_for("auth.login"))

    # Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(products)
    app.register_blueprint(suppliers)
    app.register_blueprint(sales)
    app.register_blueprint(ai)  # AI Assistant

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)