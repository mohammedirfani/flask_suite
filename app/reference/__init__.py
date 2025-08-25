
from flask import Blueprint, render_template
bp = Blueprint("reference", __name__, template_folder="templates", static_folder="static")
from . import routes

@bp.get("/")
def home():
    tiles = [{'title': 'Circuit Inventory', 'desc': 'Circuit inventory dashboard.', 'href': '/reference/circuit-inventory', 'icon': 'usb-c'},
             {'title': 'HW Inventory', 'desc': 'Hardware inventory dashboard.', 'href': '/reference/hw-inventory', 'icon': 'pc-display'}]
    return render_template("reference/home.html", title="Reference", tiles=tiles)
