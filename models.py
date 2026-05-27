"""
models.py — Database models for Event Reminder App
Defines the Event table using Flask-SQLAlchemy ORM.
"""

from extensions import db
from datetime import datetime


class Event(db.Model):
    """Represents a single calendar event stored in the database."""

    __tablename__ = "events"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(150), nullable=False)
    date        = db.Column(db.Date,        nullable=False)
    time        = db.Column(db.Time,        nullable=False)
    description = db.Column(db.Text,        nullable=True, default="")
    created_at  = db.Column(db.DateTime,    default=datetime.utcnow)

    @property
    def datetime(self):
        """Return a combined datetime object for easy comparison."""
        return datetime.combine(self.date, self.time)

    def __repr__(self):
        return f"<Event {self.id}: {self.title} on {self.date} at {self.time}>"
