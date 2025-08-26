# app/cucm_report/ris_report.py
from flask import Blueprint, render_template

ris_report_bp = Blueprint(
    "ris_report",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/cucm_report/ris_report"
)

@ris_report_bp.route("/")
def index():
    """
    Landing page for RIS Report.
    Later you can extend this to query CUCM RIS service or import/export CSV.
    """
    return render_template("cucm_report/ris_report/index.html", title="RIS Report")
