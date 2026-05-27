"""
routes.py — URL route handlers for Event Reminder App
Handles: dashboard, add event, delete event.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Event
from datetime import datetime, date, timedelta

# Create a Blueprint so routes stay separate from app factory
main = Blueprint("main", __name__)


@main.route("/")
def dashboard():
    """
    Dashboard: show upcoming events sorted by date/time.
    Events in the next 24 hours are flagged as 'soon'.
    """
    now  = datetime.now()
    soon = now + timedelta(hours=24)

    # All future events sorted ascending
    all_events = (
        Event.query
        .filter(Event.date >= date.today())
        .order_by(Event.date.asc(), Event.time.asc())
        .all()
    )

    # Split into "happening soon" vs regular upcoming
    upcoming_soon    = [e for e in all_events if now <= e.datetime <= soon]
    upcoming_regular = [e for e in all_events if e.datetime > soon]

    # Past events (just in case user wants to see them too)
    past_events = (
        Event.query
        .filter(Event.date < date.today())
        .order_by(Event.date.desc(), Event.time.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        upcoming_soon=upcoming_soon,
        upcoming_regular=upcoming_regular,
        past_events=past_events,
        now=now,
    )


@main.route("/add", methods=["GET", "POST"])
def add_event():
    """Show add-event form (GET) and save new event to DB (POST)."""
    if request.method == "POST":
        title       = request.form.get("title", "").strip()
        date_str    = request.form.get("date", "").strip()
        time_str    = request.form.get("time", "").strip()
        description = request.form.get("description", "").strip()

        # --- Basic validation ---
        errors = []
        if not title:
            errors.append("Event title is required.")
        if not date_str:
            errors.append("Date is required.")
        if not time_str:
            errors.append("Time is required.")

        event_date = None
        event_time = None

        if date_str:
            try:
                event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                errors.append("Invalid date format.")

        if time_str:
            try:
                event_time = datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                errors.append("Invalid time format.")

        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template("add_event.html", form_data=request.form)

        # --- Save to database ---
        new_event = Event(
            title=title,
            date=event_date,
            time=event_time,
            description=description,
        )
        db.session.add(new_event)
        db.session.commit()

        flash(f'✅ Event "{title}" added successfully!', "success")
        return redirect(url_for("main.dashboard"))

    # GET — render blank form
    return render_template("add_event.html", form_data={})


@main.route("/delete/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    """Delete an event by ID."""
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash(f'🗑️ Event "{event.title}" deleted.', "info")
    return redirect(url_for("main.dashboard"))
