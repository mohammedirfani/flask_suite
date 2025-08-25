
from flask import Blueprint, render_template
bp = Blueprint("ios_tool", __name__, template_folder="templates", static_folder="static")
from . import routes

@bp.get("/")
def home():
    tiles = [{'title': 'MGCP/SCCP Bouncing', 'desc': 'Restart voice services (placeholder).', 'href': '/ios-tool/mgcp-sccp-bounce', 'icon': 'arrow-repeat'}, {'title': 'Interface Bouncing', 'desc': 'Shut/no shut interfaces (placeholder).', 'href': '/ios-tool/interface-bounce', 'icon': 'arrows-collapse'}]
    return render_template("ios_tool/home.html", title="IOS Tool", tiles=tiles)
