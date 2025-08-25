from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint("auth", __name__, template_folder="templates")

@auth_bp.get("/login")
def login_form():
    return render_template("auth/login.html", title="Admin Login")

@auth_bp.post("/login")
def login():
    user = (request.form.get("username") or "").strip()
    pwd  = (request.form.get("password") or "").strip()
    if user == "admin" and pwd == "admin":
        session["is_admin"] = True
        flash("Admin mode enabled.", "success")
        return redirect(url_for("personal.home"))
    flash("Invalid credentials.", "danger")
    return redirect(url_for("auth.login_form"))

@auth_bp.get("/logout")
def logout():
    session.pop("is_admin", None)
    flash("Admin mode disabled.", "info")
    return redirect(url_for("personal.home"))
