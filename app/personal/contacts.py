from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session, send_file, current_app
)
import csv, io
from pathlib import Path
import re

contacts_bp = Blueprint(
    "contacts",
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ===== CSV persistence =====
CSV_HEADERS = ["name", "email", "phone", "company", "role", "remarks"]

def _csv_path() -> Path:
    cfg = current_app.config
    data_dir = Path(cfg["DATA_DIR"])
    data_dir.mkdir(parents=True, exist_ok=True)
    p = Path(cfg.get("CONTACTS_CSV") or (data_dir / "contacts.csv"))
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def _load_rows() -> list[dict]:
    path = _csv_path()
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append({
                "name":    (row.get("name") or "").strip(),
                "email":   (row.get("email") or "").strip(),
                "phone":   (row.get("phone") or "").strip(),
                "company": (row.get("company") or "").strip(),
                "role":    (row.get("role") or "").strip(),
                "remarks": (row.get("remarks") or "").strip(),
            })
    return rows

def _save_rows(rows: list[dict]) -> None:
    path = _csv_path()
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        w.writeheader()
        for r in rows:
            w.writerow({
                "name":    r.get("name",""),
                "email":   r.get("email",""),
                "phone":   r.get("phone",""),
                "company": r.get("company",""),
                "role":    r.get("role",""),
                "remarks": r.get("remarks",""),
            })
    tmp.replace(path)

# ===== utils =====
EMAIL_RE = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.IGNORECASE)

def _valid_email(s: str) -> bool:
    return bool(EMAIL_RE.match((s or "").strip()))

def _norm_email(s: str) -> str:
    """Normalize email for duplicate detection."""
    return (s or "").strip().lower()

def _email_exists(rows: list[dict], email_norm: str) -> bool:
    return any(_norm_email(r.get("email")) == email_norm for r in rows)

# ===== views =====
@contacts_bp.get("/")
def index():
    q = (request.args.get("q") or "").strip().lower()
    company = request.args.get("company")
    rows = _load_rows()

    # Filter by search
    if q:
        def match(r):
            return " ".join([
                r.get("name",""), r.get("email",""), r.get("phone",""),
                r.get("company",""), r.get("role",""), r.get("remarks","")
            ]).lower()
        rows = [r for r in rows if q in match(r)]

    # Filter by company (sidebar)
    if company:
        rows = [r for r in rows if (r.get("company") or "") == company]

    companies = sorted({r.get("company","") for r in _load_rows() if r.get("company")})

    return render_template(
        "personal/contacts/index.html",
        title="Contacts",
        rows=rows,
        q=q,
        companies=companies,
        active_company=company
    )

@contacts_bp.post("/add")
def add_one():
    if not session.get("is_admin"):
        flash("Admin required.", "warning")
        return redirect(url_for("contacts.index"))

    name    = (request.form.get("name") or "").strip()
    email   = (request.form.get("email") or "").strip()
    phone   = (request.form.get("phone") or "").strip()
    company = (request.form.get("company") or "").strip()
    role    = (request.form.get("role") or "").strip()
    remarks = (request.form.get("remarks") or "").strip()

    if not email:
        flash("Email is required.", "warning")
        return redirect(url_for("contacts.index"))
    if not _valid_email(email):
        flash("Invalid email address.", "danger")
        return redirect(url_for("contacts.index"))

    email_norm = _norm_email(email)
    rows = _load_rows()
    if _email_exists(rows, email_norm):
        flash("That email already exists in Contacts.", "warning")
        return redirect(url_for("contacts.index"))

    rows.append({
        "name": name,
        "email": email_norm,     # store normalized
        "phone": phone,
        "company": company,
        "role": role,
        "remarks": remarks,
    })
    _save_rows(rows)
    flash("Contact added (saved to CSV).", "success")
    return redirect(url_for("contacts.index"))


@contacts_bp.post("/import")
def import_csv():
    if not session.get("is_admin"):
        flash("Admin required.", "warning")
        return redirect(url_for("contacts.index"))

    f = request.files.get("file")
    if not f or f.filename == "":
        flash("Please choose a CSV file.", "warning")
        return redirect(url_for("contacts.index"))

    existing = _load_rows()
    added = skipped_invalid = skipped_duplicates = 0

    try:
        s = io.StringIO(f.stream.read().decode("utf-8", errors="ignore"))
        r = csv.DictReader(s)
        for row in r:
            email_raw = (row.get("email") or "").strip()
            if not email_raw or not _valid_email(email_raw):
                skipped_invalid += 1
                continue

            email_norm = _norm_email(email_raw)
            if _email_exists(existing, email_norm):
                skipped_duplicates += 1
                continue

            existing.append({
                "name":    (row.get("name") or "").strip(),
                "email":   email_norm,  # store normalized
                "phone":   (row.get("phone") or "").strip(),
                "company": (row.get("company") or "").strip(),
                "role":    (row.get("role") or "").strip(),
                "remarks": (row.get("remarks") or "").strip(),
            })
            added += 1

        _save_rows(existing)
        if added:
            flash(f"Imported {added} contact(s).", "success")
        if skipped_duplicates:
            flash(f"Skipped {skipped_duplicates} duplicate email(s).", "warning")
        if skipped_invalid:
            flash(f"Skipped {skipped_invalid} invalid row(s).", "danger")
        if not (added or skipped_duplicates or skipped_invalid):
            flash("No rows processed from the CSV.", "warning")

    except Exception as e:
        flash(f"Import failed: {e}", "danger")

    return redirect(url_for("contacts.index"))


@contacts_bp.get("/export")
def export_csv():
    path = _csv_path()
    if not path.exists():
        _save_rows([])
    return send_file(
        str(path),
        mimetype="text/csv",
        as_attachment=True,
        download_name="contacts_export.csv"
    )

@contacts_bp.get("/_migrate_contacts_normalize")
def migrate_contacts_normalize():
    rows = _load_rows()
    seen = set()
    new_rows = []
    dup = 0
    for r in rows:
        em = _norm_email(r.get("email"))
        if not em or em in seen:
            dup += 1
            continue
        seen.add(em)
        new_rows.append({
            "name": r.get("name","").strip(),
            "email": em,  # normalized
            "phone": r.get("phone","").strip(),
            "company": r.get("company","").strip(),
            "role": r.get("role","").strip(),
            "remarks": r.get("remarks","").strip(),
        })
    _save_rows(new_rows)
    flash(f"Normalization complete. Removed {dup} duplicate/empty email rows.", "success")
    return redirect(url_for("contacts.index"))
