# app/__init__.py
from flask import Flask, render_template, session
from .extensions import register_extensions
from pathlib import Path


def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret"   # ⚠️ change in production
    register_extensions(app)

    # === Data directory (instance/data) ===
    data_dir = Path(app.instance_path) / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    app.config["DATA_DIR"] = str(data_dir)  # e.g., /.../instance/data
    # Optional: override file path via env or config file
    app.config.setdefault("FAVORITES_CSV", str(data_dir / "favorites.csv"))
    app.config.setdefault("CONTACTS_CSV", str(data_dir / "contacts.csv"))

    # === Blueprints ===
    # Personal + sub-apps
    from .personal import bp as personal_bp
    from .personal.favorites import favorites_bp
    from .personal.contacts import contacts_bp

    # cucm_report + sub-apps
    from .cucm_report import bp as cucm_report_bp
    from .cucm_report.sip_trunk import sip_trunk_bp
    from .cucm_report.ris_report import ris_report_bp
    from .cucm_report.phone_dn_report import phone_dn_report_bp

    # Other app groups
    from .reference import bp as reference_bp
    from .cucm_tool import bp as cucm_tool_bp
    from .ios_report import bp as ios_report_bp
    from .ios_tool import bp as ios_tool_bp

    # Auth (admin login/logout)
    from .auth import auth_bp

    # Register blueprints
    app.register_blueprint(personal_bp,  url_prefix="/personal")
    app.register_blueprint(favorites_bp, url_prefix="/personal/favorites")
    app.register_blueprint(contacts_bp,  url_prefix="/personal/contacts")

    app.register_blueprint(cucm_report_bp, url_prefix="/cucm_report")
    app.register_blueprint(sip_trunk_bp, url_prefix="/cucm_report/sip_trunk")
    app.register_blueprint(ris_report_bp, url_prefix="/cucm_report/ris_report")
    app.register_blueprint(phone_dn_report_bp, url_prefix="/cucm_report/phone_dn_report")


    app.register_blueprint(reference_bp,   url_prefix="/reference")
    app.register_blueprint(cucm_tool_bp,   url_prefix="/cucm-tool")
    app.register_blueprint(ios_report_bp,  url_prefix="/ios-report")
    app.register_blueprint(ios_tool_bp,    url_prefix="/ios-tool")

    app.register_blueprint(auth_bp,        url_prefix="/auth")

    # Make `is_admin` available to all templates
    @app.context_processor
    def inject_flags():
        return {"is_admin": bool(session.get("is_admin"))}

    # === Landing page ===
    @app.get("/")
    def index():
        tiles = [
            {"title": "Personal",    "desc": "Favorites & Contacts",      "href": "/personal",     "icon": "person-lines-fill"},
            {"title": "Reference",   "desc": "Circuit & HW Inventory",    "href": "/reference",    "icon": "journals"},
            {"title": "CUCM Report", "desc": "SIP Trunk & RIS Report",    "href": "/cucm_report",  "icon": "file-earmark-bar-graph"},
            {"title": "CUCM Tool",   "desc": "AA & EM Tools",             "href": "/cucm-tool",    "icon": "cpu"},
            {"title": "IOS Report",  "desc": "VLAN & Interface Details",  "href": "/ios-report",   "icon": "clipboard-data"},
            {"title": "IOS Tool",    "desc": "MGCP/SCCP & Intf Bounce",   "href": "/ios-tool",     "icon": "wrench-adjustable"},
        ]
        return render_template("index.html", tiles=tiles, title="Suite Home")

    return app
