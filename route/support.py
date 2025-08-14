from app import app,request,render_template


@app.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        return f'<h1>{name},{email},{subject} {message}</h1>'

    else:
        return render_template('support.html')
