from flask import render_template
from . import bp


@bp.get("/sip-trunk")
def sip_trunk():
    return render_template("cucm_report/sip-trunk.html", title="SIP Trunk")


@bp.get("/ris-report")
def ris_report():
    return render_template("cucm_report/ris-report.html", title="RIS Report")
