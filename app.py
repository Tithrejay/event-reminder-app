"""
app.py — Flask Application Factory for Event Reminder App
Run with: python app.py
"""

import os
from flask import Flask
from extensions import db


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # ── Configuration ──────────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///database.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── Initialise extensions ──────────────────────────────────────────────────
    db.init_app(app)

    # ── Register blueprints ────────────────────────────────────────────────────
    from routes import main
    app.register_blueprint(main)

    # ── Create database tables on first run ────────────────────────────────────
    with app.app_context():
        db.create_all()

    return app


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = create_app()
    print("\n🚀  Event Reminder App is running!")
    print("📍  Open: http://127.0.0.1:5000\n")
    app.run(debug=True)
