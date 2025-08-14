import sqlite3
from itertools import product

from app import app,render_template
import requests

path='/static/img/'



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



@app.route('/Samsung')
def Samsung():  # put application's code here
    connection = sqlite3.connect("test.sqlite3")
    cursor = connection.cursor()
    result = cursor.execute("select * from phone where brand='Samsung'").fetchall()
    data = []
    title=''
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
        title=i[2]
        data.append(product)

    return render_template('men.html', data=data, title=title)

@app.route('/Apple')
def Apple():  # put application's code here
    connection = sqlite3.connect("test.sqlite3")
    cursor = connection.cursor()
    result = cursor.execute("select * from phone where brand='Apple'").fetchall()
    data = []
    title = ''
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

    return render_template('men.html', data=data, title=title)

@app.route('/Xiaomi')
def Xiaomi():  # put application's code here
    connection = sqlite3.connect("test.sqlite3")
    cursor = connection.cursor()
    result = cursor.execute("select * from phone where brand='Xiaomi'").fetchall()
    data = []
    title = ''
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

    return render_template('men.html', data=data, title=title)

@app.route('/Vivo')
def Vivo():  # put application's code here
    connection = sqlite3.connect("test.sqlite3")
    cursor = connection.cursor()
    result = cursor.execute("select * from phone where brand='Vivo'").fetchall()
    data = []
    title = ''
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

    return render_template('men.html', data=data, title=title)

@app.route('/Oppo')
def Oppo():  # put application's code here
    connection = sqlite3.connect("test.sqlite3")
    cursor = connection.cursor()
    result = cursor.execute("select * from phone where brand='Oppo'").fetchall()
    data = []
    title = ''
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

    return render_template('men.html', data=data, title=title)