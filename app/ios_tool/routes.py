from flask import render_template
from . import bp


@bp.get("/mgcp-sccp-bounce")
def mgcp_sccp_bounce():
    return render_template("ios_tool/mgcp-sccp-bounce.html", title="MGCP/SCCP Bouncing")


@bp.get("/interface-bounce")
def interface_bounce():
    return render_template("ios_tool/interface-bounce.html", title="Interface Bouncing")
