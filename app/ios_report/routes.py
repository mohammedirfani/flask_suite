from flask import render_template
from . import bp


@bp.get("/vlan-report")
def vlan_report():
    return render_template("ios_report/vlan-report.html", title="VLAN Report")


@bp.get("/interface-details")
def interface_details():
    return render_template("ios_report/interface-details.html", title="Interface Details")
