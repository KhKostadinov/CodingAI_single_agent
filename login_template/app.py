"""
app.py
------
Main Flask application for the login system.
Provides routes for registration, login, logout, and dashboard.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from functools import wraps
import os

from database import db, User, init_db

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # SQLite database configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'app.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    init_db(app)

    register_routes(app)
    return app


# ---------------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------------
def login_required(f):
    """Redirect to login page if the user is not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Route registration
# ---------------------------------------------------------------------------
def register_routes(app: Flask) -> None:

    # ---- Home / redirect ----
    @app.route("/")
    def index():
        if "user_id" in session:
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    # ---- Login ----
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            if not username or not password:
                flash("Please fill in all fields.", "error")
                return render_template("login.html")

            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                session["user_id"] = user.id
                session["username"] = user.username
                user.last_login = datetime.utcnow()
                db.session.commit()
                flash("Welcome back, " + user.username + "!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid username or password.", "error")
                return render_template("login.html")

        return render_template("login.html")

    # ---- Register ----
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            confirm = request.form.get("confirm_password", "")

            # Validation
            errors = []
            if len(username) < 3:
                errors.append("Username must be at least 3 characters.")
            if not email or "@" not in email:
                errors.append("Please provide a valid email address.")
            if len(password) < 6:
                errors.append("Password must be at least 6 characters.")
            if password != confirm:
                errors.append("Passwords do not match.")

            if errors:
                for e in errors:
                    flash(e, "error")
                return render_template("register.html")

            # Check uniqueness
            if User.query.filter_by(username=username).first():
                flash("Username already taken.", "error")
                return render_template("register.html")
            if User.query.filter_by(email=email).first():
                flash("Email already registered.", "error")
                return render_template("register.html")

            # Create user
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    # ---- Dashboard (protected) ----
    @app.route("/dashboard")
    @login_required
    def dashboard():
        user = User.query.get(session["user_id"])
        return render_template("dashboard.html", user=user)

    # ---- Logout ----
    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been logged out.", "success")
        return redirect(url_for("login"))

    # ---- API: verify session (useful for SPA-style checks) ----
    @app.route("/api/session", methods=["GET"])
    def api_session():
        if "user_id" in session:
            user = User.query.get(session["user_id"])
            return jsonify({"authenticated": True, "user": user.to_dict()})
        return jsonify({"authenticated": False})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
