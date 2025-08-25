
from flask import Blueprint, render_template
bp = Blueprint("ios_report", __name__, template_folder="templates", static_folder="static")
from . import routes

@bp.get("/")
def home():
    tiles = [{'title': 'VLAN Report', 'desc': 'VLAN inventory and status.', 'href': '/ios-report/vlan-report', 'icon': 'diagram-2'}, {'title': 'Interface Details', 'desc': 'Switch/Router interface details.', 'href': '/ios-report/interface-details', 'icon': 'hdd-network'}]
    return render_template("ios_report/home.html", title="IOS Report", tiles=tiles)
