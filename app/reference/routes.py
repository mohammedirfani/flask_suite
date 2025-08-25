from flask import render_template
from . import bp


@bp.get("/circuit-inventory")
def circuit_inventory():
    return render_template("reference/circuit-inventory.html", title="Circuit Inventory")


@bp.get("/hw-inventory")
def hw_inventory():
    return render_template("reference/hw-inventory.html", title="HW Inventory")
