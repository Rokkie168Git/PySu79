from app import app,request,render_template


@app.route('/pagecart', methods=['GET', 'POST'])
def pagecart():


    return render_template('cart.html',)
