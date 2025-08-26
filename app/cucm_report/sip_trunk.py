
# app/cucm_report/sip_trunk.py
from flask import Blueprint, render_template

sip_trunk_bp = Blueprint(
    "sip_trunk",                      # <-- blueprint name (used in url_for)
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/cucm_report/sip_trunk"  # final URL path
)

@sip_trunk_bp.route("/")
def index():
    return render_template("cucm_report/sip_trunk/index.html", title="SIP Trunk Report")
