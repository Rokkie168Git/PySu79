import os, uuid, pathlib, sqlite3
from flask import request, render_template, redirect, url_for, abort, flash
from werkzeug.utils import secure_filename

from app import app,render_template





IMAGE_SUBDIR   = "img"                                # <— matches /static/img
STATIC_IMG_DIR = os.path.join(app.static_folder, IMAGE_SUBDIR)
os.makedirs(STATIC_IMG_DIR, exist_ok=True)

ALLOWED_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def _save_image(file_storage):
    if not file_storage or not file_storage.filename:
        return ""
    fname = secure_filename(file_storage.filename)
    ext = pathlib.Path(fname).suffix.lower()
    if ext not in ALLOWED_EXTS:
        raise ValueError("Unsupported image type.")
    unique = f"{uuid.uuid4().hex}{ext}"
    file_storage.save(os.path.join(STATIC_IMG_DIR, unique))
    return unique

def allowed(filename: str) -> bool:
    return pathlib.Path(filename).suffix.lower() in ALLOWED_EXTS
def save_image(file_storage):

    if not file_storage or not file_storage.filename:
        return ""
    fname = secure_filename(file_storage.filename)
    ext = pathlib.Path(fname).suffix.lower()
    if ext not in ALLOWED_EXTS:
        raise ValueError("Unsupported image type")
    unique = f"{uuid.uuid4().hex}{ext}"
    file_storage.save(os.path.join(STATIC_IMG_DIR, unique))
    return unique

# ---- Database ----
DB_PATH = "test.sqlite3"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn



# ---- Routes ----
@app.route("/phones/add", methods=["GET", "POST"])
def add_phone():
    if request.method == "POST":
        f = request.form
        errors = []

        # required text/number fields
        required_fields = [
            "name","brand","model","price","quantity","warranty_mo","os","cpu",
            "ram_gb","storage_gb","display","cameras","battery_mah","network",
            "color","highlights","description","available","type"
        ]
        for key in required_fields:
            if not (f.get(key) or "").strip():
                errors.append(f"{key.replace('_',' ').title()} is required.")

        # cast numbers safely
        try: price = float(f.get("price", "0"))
        except: errors.append("Price must be a number.")
        try: quantity = int(f.get("quantity", "0"))
        except: errors.append("Quantity must be an integer.")
        try: warranty_mo = int(f.get("warranty_mo", "12"))
        except: errors.append("Warranty (months) must be an integer.")
        try: ram_gb = int(f.get("ram_gb", "0"))
        except: errors.append("RAM (GB) must be an integer.")
        try: storage_gb = int(f.get("storage_gb", "0"))
        except: errors.append("Storage (GB) must be an integer.")
        try: battery_mah = int(f.get("battery_mah", "0"))
        except: errors.append("Battery (mAh) must be an integer.")

        # files
        main_file = request.files.get("main_image")
        side_file = request.files.get("side_image")
        sub_file  = request.files.get("sub_image")

        if not main_file or not main_file.filename:
            errors.append("Main image is required.")
        if not side_file or not side_file.filename:
            errors.append("Side image is required.")
        if not sub_file or not sub_file.filename:
            errors.append("Sub image is required.")

        if errors:
            return render_template("phone_add.html", errors=errors, data=f)

        try:
            main_image = save_image(main_file)
            side_image = save_image(side_file)
            sub_image  = save_image(sub_file)
        except Exception as e:
            return render_template("phone_add.html", errors=[str(e)], data=f)

        # insert
        with get_conn() as conn:
            cur = conn.execute("""
                INSERT INTO phone
                (name, brand, model, price, quantity, warranty_mo, os, cpu, ram_gb, storage_gb,
                 display, cameras, battery_mah, network, color, highlights, description,
                 available, main_image, side_image, sub_image, type)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                f["name"].strip(), f["brand"].strip(), f["model"].strip(),
                price, quantity, warranty_mo, f["os"].strip(), f["cpu"].strip(),
                ram_gb, storage_gb, f["display"].strip(), f["cameras"].strip(),
                battery_mah, f["network"].strip(), f["color"].strip(),
                f["highlights"].strip(), f["description"].strip(),
                f["available"], main_image, side_image, sub_image, f["type"].strip()
            ))
            phone_id = cur.lastrowid

        return redirect(url_for("add_phone", phone_id=phone_id))

    # GET
    return render_template("phone_add.html", errors=None, data={})





def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/phones")
def phone_list():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM phone ORDER BY id DESC").fetchall()
        q = conn.execute("SELECT SUM(quantity) FROM phone").fetchone()[0]


    return render_template("phone_list.html", phones=rows, q=q)

@app.route("/phones/delete/<int:phone_id>", methods=["POST"])
def phone_delete(phone_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM phone WHERE id = ?", (phone_id,))
    return redirect(url_for("phone_list"))
@app.route("/phones/update/<int:phone_id>", methods=["GET", "POST"])
def phone_update(phone_id):
    # Load current row
    with get_conn() as conn:
        phone = conn.execute("SELECT * FROM phone WHERE id = ?", (phone_id,)).fetchone()
    if not phone:
        abort(404)

    if request.method == "POST":
        f = request.form
        def to_int(k, d=0):
            try: return int(f.get(k, d))
            except: return d
        def to_float(k, d=0.0):
            try: return float(f.get(k, d))
            except: return d

        # Text & number fields (same as you had)
        name        = (f.get("name") or "").strip()
        brand       = (f.get("brand") or "").strip()
        model       = (f.get("model") or "").strip()
        price       = to_float("price")
        quantity    = to_int("quantity")
        warranty_mo = to_int("warranty_mo", 12)
        os_name     = (f.get("os") or "").strip()
        cpu         = (f.get("cpu") or "").strip()
        ram_gb      = to_int("ram_gb")
        storage_gb  = to_int("storage_gb")
        display     = (f.get("display") or "").strip()
        cameras     = (f.get("cameras") or "").strip()
        battery_mah = to_int("battery_mah")
        network     = (f.get("network") or "").strip()
        color       = (f.get("color") or "").strip()
        highlights  = (f.get("highlights") or "").strip()
        description = (f.get("description") or "").strip()
        available   = (f.get("available") or "in_stock").strip()
        type_       = (f.get("type") or "smartphone").strip()

        # Files coming from the form (names must match your <input name="...">)
        main_fs = request.files.get("main_image")
        side_fs = request.files.get("side_image")
        sub_fs  = request.files.get("sub_image")

        # Try saving new files (if provided)
        try:
            new_main = _save_image(main_fs) if main_fs and main_fs.filename else ""
            new_side = _save_image(side_fs) if side_fs and side_fs.filename else ""
            new_sub  = _save_image(sub_fs)  if sub_fs  and sub_fs.filename  else ""
        except Exception as e:
            # Re-render with error; keep current values
            return render_template("phone_update.html", phone=phone, errors=[str(e)])

        # If no new image uploaded for a field, keep old one
        main_image = new_main or phone["main_image"]
        side_image = new_side or phone["side_image"]
        sub_image  = new_sub  or phone["sub_image"]

        # Update DB (including possibly new image filenames)
        with get_conn() as conn:
            cur = conn.execute("""
                UPDATE phone SET
                  name=?, brand=?, model=?, price=?, quantity=?, warranty_mo=?,
                  os=?, cpu=?, ram_gb=?, storage_gb=?, display=?, cameras=?,
                  battery_mah=?, network=?, color=?, highlights=?, description=?,
                  available=?, main_image=?, side_image=?, sub_image=?, type=?,
                  updated_at=datetime('now')
                WHERE id=?
            """, (
                name, brand, model, price, quantity, warranty_mo,
                os_name, cpu, ram_gb, storage_gb, display, cameras,
                battery_mah, network, color, highlights, description,
                available, main_image, side_image, sub_image, type_,
                phone_id
            ))

        # Delete old files only if replacement actually happened
        def _remove_old(old_name, new_name):
            if new_name and old_name and old_name != new_name:
                old_path = os.path.join(STATIC_IMG_DIR, old_name)
                try:
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    # ignore delete errors
                    pass

        _remove_old(phone["main_image"], new_main)
        _remove_old(phone["side_image"], new_side)
        _remove_old(phone["sub_image"],  new_sub)

        return redirect(url_for("phone_list"))

    # GET → show form
    return render_template("phone_update.html", phone=phone, errors=None, IMAGE_SUBDIR=IMAGE_SUBDIR)

@app.route("/admin")
def admin():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM phone ORDER BY id DESC").fetchall()
        data = []
        for i in rows:
            product = {
                'id': i[0],
                'name': i[1],
                'brand': i[2],
                'model': i[3],
                'price': i[4],
                'quantity': i[5],
                'warranty': i[6],
                'os': i[7],
                'cpu': i[8],
                'ram': i[9],
                'storage': i[10],
                'display': i[11],
                'camera': i[12],
                'battery': i[13],
                'network': i[14],
                'color': i[15],
                'highlight': i[16],
                'description': i[17],
                'available': i[18],
                'main_image': path + i[19],
                'side_image': path + i[20],
                'sub_image': path + i[21],
                'type': i[22],
            }
            data.append(product)

    return render_template(
        "dashboard.html",phones=rows,
    )

path='/static/img/'
@app.route("/login_admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "Admin" and password == "123":
            return redirect(url_for("admin"))
        else:
            return render_template("login_admin.html", error=True)

    return render_template("login_admin.html", error=False)

@app.route("/dashboard")
def dashboard():
    # pass whatever data you like; these are optional
    return render_template(
        "dashboard.html",

    )
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    connection = sqlite3.connect("test.sqlite3")
    cursor = connection.cursor()
    result = cursor.execute(f"select * from phone where id={product_id}").fetchall()
    phone = []
    for i in result:
        product = {
            'id': i[0],
            'name': i[1],
            'brand': i[2],
            'model': i[3],
            'price': i[4],
            'quantity': i[5],
            'warranty': i[6],
            'os': i[7],
            'cpu': i[8],
            'ram_gb': i[9],
            'storage_gb': i[10],
            'display': i[11],
            'cameras': i[12],
            'battery_mah': i[13],
            'network': i[14],
            'color': i[15],
            'highlight': i[16],
            'description': i[17],
            'available': i[18],
            'main_image': path + i[19],
            'side_image': path + i[20],
            'sub_image': path + i[21],
            'type': i[22],
        }
        phone.append(product)
    return render_template('product.html' ,phone=phone)
