from flask import Blueprint, render_template

bp = Blueprint("personal", __name__, template_folder="templates", static_folder="static")

from . import routes

# @bp.get("/")
# def home():
#     tiles = [{'title': 'Favorites', 'desc': 'Manage and search your favorite URLs.', 'href': '/personal/favorites', 'icon': 'bookmark-heart-fill'},
#              {'title': 'Contact List', 'desc': 'Contacts management area.', 'href': '/personal/contacts', 'icon': 'person-rolodex'}]
#
#     return render_template("personal/home.html", title="Personal", tiles=tiles)

