# app/personal/routes.py
from flask import render_template, redirect, url_for
from . import bp


# @bp.get("/")
# def home():
#     tiles = [{'title': 'SIP Trunk', 'desc': 'SIP trunk reporting.', 'href': '/cucm_report/sip_trunk', 'icon': 'diagram-3'},
#              {'title': 'RIS Report', 'desc': 'Realtime Information Service report.', 'href': '/cucm_report/ris_report', 'icon': 'speedometer2'}]
#     return render_template("cucm_report/home.html", title="CUCM Report", tiles=tiles)


@bp.get("/")
def home():
    """Landing page for the Personal app"""
    tiles = [{'title': 'SIP Trunk', 'desc': 'SIP trunk reporting.', 'href': '/cucm_report/sip_trunk', 'icon': 'diagram-3'},
             {'title': 'RIS Report', 'desc': 'Realtime Information Service report.', 'href': '/cucm_report/ris_report', 'icon': 'speedometer2'},
             {'title': 'Phone DN Report', 'desc': 'Phone DN report.', 'href': '/cucm_report/phone_dn_report', 'icon': 'telephone-forward'}]
    return render_template("cucm_report/home.html", title="CUCM Report", tiles=tiles)

# These two are optional helpers: they just forward /personal/favorites
# and /personal/contacts to the respective sub-blueprints.
# If you prefer, you can remove them and only use the sub-blueprints.
@bp.get("/sip_trunk")
def sip_trunk_forward():
    return redirect(url_for("sip_trunk.index"))

@bp.get("/ris_report")
def ris_report_forward():
    return redirect(url_for("ris_report.index"))

@bp.get("/phone_dn_report")
def phone_dn_report_forward():
    return redirect(url_for("phone_dn_report.index"))