# app/personal/favorites.py
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session, send_file, current_app
)
import csv, io, os
from urllib.parse import urlparse, urlunparse
from pathlib import Path

favorites_bp = Blueprint(
    "favorites",
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ===== URL helpers =====
def normalize_url(u: str) -> str:
    if not u:
        return ""
    u = u.strip()
    if not u.lower().startswith(("http://", "https://")):
        u = "https://" + u

    p = urlparse(u)
    scheme = (p.scheme or "https").lower()
    host = (p.netloc or "").strip()

    # host:port split
    if ":" in host:
        hostname, port = host.rsplit(":", 1)
    else:
        hostname, port = host, ""

    hostname = hostname.lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]

    # drop default ports
    if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
        port = ""

    netloc = f"{hostname}:{port}" if port else hostname

    path = (p.path or "")
    if path == "/":
        path = ""
    elif path.endswith("/"):
        path = path[:-1]

    return urlunparse((scheme, netloc, path, "", p.query, p.fragment))

def is_valid_url(u: str) -> bool:
    try:
        p = urlparse(u)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False

def url_exists(rows, url_norm: str) -> bool:
    for r in rows:
        if normalize_url(r.get("url", "")) == url_norm:
            return True
    return False

# ===== CSV persistence helpers =====
CSV_HEADERS = ["Category", "Alias", "URL", "Remarks"]

def _csv_path() -> Path:
    # Use config FAVORITES_CSV if provided, else DATA_DIR/favorites.csv
    cfg = current_app.config
    p = Path(cfg.get("FAVORITES_CSV") or (Path(cfg["DATA_DIR"]) / "favorites.csv"))
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
                "category": (row.get("Category") or "").strip(),
                "alias": (row.get("Alias") or "").strip(),
                "url": (row.get("URL") or "").strip(),
                "remarks": (row.get("Remarks") or "").strip(),
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
                "Category": r.get("category", ""),
                "Alias": r.get("alias", ""),
                "URL": r.get("url", ""),
                "Remarks": r.get("remarks", ""),
            })
    tmp.replace(path)

# ===== Views =====
@favorites_bp.get("/")
def index():
    rows = _load_rows()

    # Sidebar categories
    cats = sorted({(r.get("category") or "Uncategorized") for r in rows})
    active = request.args.get("category")
    if active:
        rows = [r for r in rows if (r.get("category") or "Uncategorized") == active]

    # ---- Sorting ----
    # ?sort=alias|category  &  ?order=asc|desc
    sort = (request.args.get("sort") or "").lower()
    order = (request.args.get("order") or "asc").lower()
    reverse = order == "desc"

    if sort in ("alias", "category"):
        keyfunc = (lambda r: (r.get(sort) or "").lower())
        rows = sorted(rows, key=keyfunc, reverse=reverse)

    return render_template(
        "personal/favorites/index.html",
        title="Favorites",
        rows=rows,
        categories=cats,
        active_cat=active,
        sort=sort,
        order=order,
    )

@favorites_bp.post("/add")
def add_one():
    if not session.get("is_admin"):
        flash("Admin required.", "warning")
        return redirect(url_for("favorites.index"))

    url_raw = (request.form.get("url") or "").strip()
    alias = (request.form.get("alias") or "").strip()
    category = (request.form.get("category") or "").strip()
    remarks = (request.form.get("remarks") or "").strip()

    if not url_raw:
        flash("URL is required.", "warning")
        return redirect(url_for("favorites.index"))

    url_norm = normalize_url(url_raw)
    if not is_valid_url(url_norm):
        flash("Invalid URL.", "danger")
        return redirect(url_for("favorites.index"))

    rows = _load_rows()
    if url_exists(rows, url_norm):
        flash("That URL already exists.", "warning")
        return redirect(url_for("favorites.index"))

    rows.append({"url": url_norm, "alias": alias, "category": category, "remarks": remarks})
    _save_rows(rows)
    flash("Added URL to favorites.", "success")
    return redirect(url_for("favorites.index"))

@favorites_bp.post("/import")
def import_csv():
    if not session.get("is_admin"):
        flash("Admin required.", "warning")
        return redirect(url_for("favorites.index"))

    f = request.files.get("file")
    if not f or f.filename == "":
        flash("Please choose a CSV file.", "warning")
        return redirect(url_for("favorites.index"))

    existing = _load_rows()
    added, skipped = 0, 0
    try:
        s = io.StringIO(f.stream.read().decode("utf-8", errors="ignore"))
        r = csv.DictReader(s)
        for row in r:
            url_raw = (row.get("URL") or "").strip()
            if not url_raw:
                skipped += 1
                continue
            url_norm = normalize_url(url_raw)
            if not is_valid_url(url_norm) or url_exists(existing, url_norm):
                skipped += 1
                continue
            existing.append({
                "url": url_norm,
                "alias": (row.get("Alias") or "").strip(),
                "category": (row.get("Category") or "").strip(),
                "remarks": (row.get("Remarks") or "").strip(),
            })
            added += 1
        _save_rows(existing)
        flash(f"Imported {added} favorites, skipped {skipped}.", "info")
    except Exception as e:
        flash(f"Import failed: {e}", "danger")

    return redirect(url_for("favorites.index"))


@favorites_bp.get("/export")
def export_csv():
    # You can just return the file we maintain:
    path = _csv_path()
    if not path.exists():
        # create an empty file with headers for convenience
        _save_rows([])
    return send_file(
        str(path),
        mimetype="text/csv",
        as_attachment=True,
        download_name="favorites_export.csv"
    )
