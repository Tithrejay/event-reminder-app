"""
extensions.py — Shared Flask extensions
Initialised here so app.py and models.py can both import without circular refs.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
