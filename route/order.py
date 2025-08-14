from flask import jsonify

from app import app,request,render_template


from flask_mail import Mail, Message
from collections import Counter

import requests

import io
from datetime import datetime
from xmlrpc.client import DateTime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from flask_mail import Message

TELEGRAM_BOT_TOKEN = '8013789582:AAGxWiyNblSjdUzNPmZeNzplCPrmkk4cJGk'
TELEGRAM_CHAT_ID = '1160984630'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rokkie.apk2@gmail.com'      # CHANGE to your Gmail!
app.config['MAIL_PASSWORD'] = 'ickcndobhagzoamv'           # CHANGE to your Gmail App Password!
app.config['MAIL_DEFAULT_SENDER'] = 'rokkie.apk2@gmail.com'
mail = Mail(app)
@app.route('/api/send-cart-order', methods=['POST'])
def send_cart_order():
    data = request.get_json()

    full_name = data.get('fullName', '')
    address = data.get('address', '')
    email = data.get('email', '')
    phone = data.get('phone', '')
    cart = data.get('cart', [])
    total = data.get('total', 0)

    # Make sure qty is present; default to 1
    for item in cart:
        if 'qty' not in item:
            item['qty'] = 1

    sub_total = sum(float(item['price']) * int(item['qty']) for item in cart)
    tax = round(sub_total * 0.15, 2)
    grand_total = round(sub_total + tax, 2)

    # --- 1. Send to Telegram ---
    # Text summary
    msg = f'🛒 <b>New Order Received!</b>\n\n'
    msg += f'<b>Name:</b> {full_name}\n<b>Address:</b> {address}\n<b>Email:</b> {email}\n<b>Phone:</b> {phone}\n\n'
    msg += '<b>Items:</b>\n'
    tax=15/100
    for item in cart:
        msg += f'• <b>{item["title"]}</b> x {item.get("qty",1)} - ${item["price"]}\n'
    tax = total * 15 / 100
    msg += f'\n<b>Tax: 15% </b> ${tax:.2f}'
    msg += f'\n<b>Total:</b> ${total+tax:.2f}'

    send_message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': msg,
        'parse_mode': 'HTML'
    }


    requests.post(send_message_url, data=payload)

    r = requests.get('https://fakestoreapi.com/products')
    # Each product image
    for item in cart:
        if 'image' in item and item['image']:
            send_photo_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            img_payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': f"{item['title']} (${item['price']}) x {item.get('qty', 1)}",
                'photo': item['image']  # should be a valid URL
            }

            resp = requests.post(send_photo_url, data=img_payload)
            print(resp.status_code, resp.text)


    # --- 2. Generate PDF Invoice ---
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = []
    styles = getSampleStyleSheet()
    desc_style = ParagraphStyle(
        'CartDescription',
        parent=styles['BodyText'],
        fontSize=9,
        leading=11,
        wordWrap='CJK',
        spaceAfter=2,
        spaceBefore=2,
    )

    now = datetime.now()
    invoice= now.strftime("INV-%Y%m%d-%H%M%S")

    elements.append(Paragraph('<b>RONG STORE</b>', styles['Title']))
    elements.append(Paragraph('RONG STORE', styles['Normal']))
    elements.append(Spacer(1, 16))
    elements.append(Paragraph('<b>Invoice</b>', styles['Heading1']))
    elements.append(Paragraph(f'Invoice No.: {invoice}', styles['Normal']))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f'<b>To</b> {full_name}', styles['Normal']))
    elements.append(Paragraph(f'<b>Address:</b> {address}', styles['Normal']))
    elements.append(Paragraph(f'<b>Email:</b> {email}', styles['Normal']))
    elements.append(Paragraph(f'<b>Phone:</b> {phone}', styles['Normal']))
    elements.append(Paragraph(f'<b>OrderDate:</b> {now.strftime("%Y-%m-%d %H:%M:%S")}', styles['Normal']))
    elements.append(Spacer(1, 16))

    # Table
    table_data = [['ITEM DESCRIPTION', 'PRICE', 'QTY', 'TOTAL']]
    for item in cart:
        item_total = float(item['price']) * int(item['qty'])
        desc = Paragraph(item['title'], desc_style)
        table_data.append([
            desc,
            "${:,.2f}".format(float(item['price'])),
            str(item['qty']),
            "${:,.2f}".format(item_total)
        ])

    col_widths = [260, 60, 40, 70]
    table = Table(table_data, colWidths=col_widths, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 18))

    # Totals
    right_align = ParagraphStyle(name='Right', parent=styles['Normal'], alignment=2)
    elements.append(Paragraph(f'Sub_total: <b>${sub_total:,.2f}</b>', right_align))
    elements.append(Paragraph(f'Tax_vat(15%): <b>${tax:,.2f}</b>', right_align))
    elements.append(
        Paragraph(f'<font size=12 color="blue"><b>Grand_total: ${grand_total:,.2f}</b></font>', right_align))
    elements.append(Spacer(1, 16))

    # Payment & Terms
    # elements.append(Paragraph('<b>Payment Method :</b>', styles['BodyText']))
    elements.append(Paragraph('Payments : rokkie.apk2@gmail.com', styles['BodyText']))
    elements.append(Paragraph('Card payment We Accept : RONG STORE Address SETEC .', styles['BodyText']))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph('<b>Terms & Conditions :</b>', styles['BodyText']))
    elements.append(Paragraph('Enda qui blandae explica qui omnim minima... etc.', styles['BodyText']))
    elements.append(Spacer(1, 18))
    elements.append(Paragraph('<i>Your Signature</i>', styles['Normal']))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    # --- 3. Send PDF via Email ---
    msg = Message(
        subject="Your Invoice (PDF)",
        recipients=[email],  # Send to the customer!
        body=f"Dear {full_name},\n\nPlease find attached your invoice as a PDF.\n\nBest regards,\nYour Store"
    )
    msg.attach("invoice.pdf", "application/pdf", pdf)
    mail.send(msg)



    return jsonify({'message': 'Order sent to Telegram and email!'})

