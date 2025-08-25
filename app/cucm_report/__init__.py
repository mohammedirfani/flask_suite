
from flask import Blueprint, render_template
bp = Blueprint("cucm_report", __name__, template_folder="templates", static_folder="static")
from . import routes
@bp.get("/")
def home():
    tiles = [{'title': 'SIP Trunk', 'desc': 'SIP trunk reporting.', 'href': '/cucm-report/sip-trunk', 'icon': 'diagram-3'}, {'title': 'RIS Report', 'desc': 'Realtime Information Service report.', 'href': '/cucm-report/ris-report', 'icon': 'speedometer2'}]
    return render_template("cucm_report/home.html", title="CUCM Report", tiles=tiles)
