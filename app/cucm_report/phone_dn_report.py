# app/cucm_report/phone_dn_report.py
from flask import Blueprint, render_template

phone_dn_report_bp = Blueprint(
    "phone_dn_report",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/cucm_report/phone_dn_report"
)

@phone_dn_report_bp.route("/")
def index():
    # For now, just render the page. You can later add logic to query CUCM DN data.
    return render_template("cucm_report/phone_dn_report/index.html", title="Phone DN Report")
