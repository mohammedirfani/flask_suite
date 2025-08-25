
from flask import Blueprint, render_template
bp = Blueprint("cucm_tool", __name__, template_folder="templates", static_folder="static")
from . import routes


@bp.get("/")
def home():
    tiles = [{'title': 'AA Enable/Disable', 'desc': 'Toggle Auto-Answer for DNs.', 'href': '/cucm-tool/aa', 'icon': 'toggle2-on'}, {'title': 'EM Login/Logout', 'desc': 'Extension Mobility login/logout.', 'href': '/cucm-tool/em', 'icon': 'box-arrow-in-right'}]
    return render_template("cucm_tool/home.html", title="CUCM Tool", tiles=tiles)
