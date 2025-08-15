import sqlite3
from itertools import product

from flask import request, redirect, url_for, abort

from app import app,render_template
import requests

from route.Admin import get_conn

path='/static/img/'

@app.route("/product/<int:product_id>")
def product_page(product_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM product WHERE id = ?", (product_id,)).fetchone()
    if not row:
        abort(404)
    # image is stored as filename; build a static URL to show it
    image_url = url_for("static", filename=f"img/{row['image']}")
    return render_template("product.html", p=row, image_url=image_url)

@app.route('/')
@app.route('/catalog')
def catalog():  # put application's code here
    connection = sqlite3.connect("test.sqlite3")
    cursor = connection.cursor()
    result  = cursor.execute("select * from phone").fetchall()
    data=[]
    for i in result:
        product={
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
            'main_image': path+i[19],
            'side_image': path+i[20],
            'sub_image': path+i[21],
            'type': i[22],
        }
        data.append(product)

    return render_template('catalog.html', data=data)


@app.route('/brand/<string:name>')
def brand(name):
    # TIP: if you already have get_conn(), use it for consistency:
    # with get_conn() as conn:
    import sqlite3

    # Make rows dict-like: row['brand'], row['price'], etc.
    conn = sqlite3.connect("test.sqlite3")
    conn.row_factory = sqlite3.Row
    with conn:
        result = conn.execute(
            "SELECT * FROM phone WHERE brand = ? COLLATE NOCASE",
            (name,)
        ).fetchall()

    # Build response data (light touch—keep keys you actually use)
    data = []
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
        title = i[2]
        data.append(product)


    # Optional: show a nice empty state if no rows
    return render_template("Brand.html", data=data, title=title)



@app.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.form['search']
    return redirect(url_for('keyword', keyword=keyword))
@app.route('/search/<string:keyword>', methods=['GET', 'POST'])
def keyword(keyword):
    connection = sqlite3.connect("test.sqlite3")
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM phone WHERE name LIKE ? COLLATE NOCASE",
                            (f"%{keyword}%",)).fetchall()
    data = []
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

    return render_template('search.html', data=data, title=keyword)