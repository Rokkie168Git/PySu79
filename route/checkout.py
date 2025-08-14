from app import app,request,render_template


@app.route('/Checkout')
def Checkout():
    return render_template('Checkout.html')
