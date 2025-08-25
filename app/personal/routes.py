# app/personal/routes.py
from flask import render_template, redirect, url_for
from . import bp

@bp.get("/")
def home():
    """Landing page for the Personal app"""
    tiles = [
        {
            "title": "Favorites",
            "desc": "Manage favorite URLs (CSV import/export, sidebar by category, live search)",
            "href": "/personal/favorites",
            "icon": "bookmark-heart-fill",
        },
        {
            "title": "Contact List",
            "desc": "Manage contacts (CSV import/export, filters, multi-email copy, tel links)",
            "href": "/personal/contacts",
            "icon": "person-rolodex",
        },
    ]
    return render_template("personal/home.html", title="Personal", tiles=tiles)


# These two are optional helpers: they just forward /personal/favorites
# and /personal/contacts to the respective sub-blueprints.
# If you prefer, you can remove them and only use the sub-blueprints.
@bp.get("/favorites")
def favorites_forward():
    return redirect(url_for("favorites.index"))

@bp.get("/contacts")
def contacts_forward():
    return redirect(url_for("contacts.index"))
