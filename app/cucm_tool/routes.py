from flask import render_template
from . import bp


@bp.get("/aa")
def aa():
    return render_template("cucm_tool/aa.html", title="AA Enable/Disable")


@bp.get("/em")
def em():
    return render_template("cucm_tool/em.html", title="EM Login/Logout")
