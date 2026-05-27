/**
 * main.js — Remindly Event App
 * Small enhancements: auto-dismiss flash messages, set min date on form.
 */

document.addEventListener("DOMContentLoaded", () => {

  // ── Auto-dismiss flash messages after 4 seconds ──────────────────────────
  const flashes = document.querySelectorAll(".flash");
  flashes.forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
      el.style.opacity = "0";
      el.style.transform = "translateY(-6px)";
      setTimeout(() => el.remove(), 500);
    }, 4000);
  });

  // ── Set minimum date to today on the date input ──────────────────────────
  const dateInput = document.getElementById("date");
  if (dateInput) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.setAttribute("min", today);
    // Pre-fill today if empty
    if (!dateInput.value) {
      dateInput.value = today;
    }
  }

  // ── Pre-fill current time (rounded to next 30 min) ───────────────────────
  const timeInput = document.getElementById("time");
  if (timeInput && !timeInput.value) {
    const now = new Date();
    const minutes = now.getMinutes();
    const roundedMinutes = minutes < 30 ? 30 : 0;
    const roundedHours = minutes < 30 ? now.getHours() : (now.getHours() + 1) % 24;
    timeInput.value = `${String(roundedHours).padStart(2, "0")}:${String(roundedMinutes).padStart(2, "0")}`;
  }

  // ── Stagger card animations ───────────────────────────────────────────────
  const cards = document.querySelectorAll(".card");
  cards.forEach((card, i) => {
    card.style.animationDelay = `${i * 60}ms`;
  });

});
