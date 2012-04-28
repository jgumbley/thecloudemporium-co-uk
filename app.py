from flaskext.wtf.html5 import EmailField
import os
from flask import Flask
from flask import render_template
from wtforms.fields.simple import TextAreaField

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/products.html')
def products():
    return render_template('products.html')

@app.route('/marshmallows.html')
def marshmallows():
    return render_template('marshmallows.html')

from flaskext.wtf import Form, TextField, Required

class Enquiry(Form):
    cust_name = TextField("customer-name", validators=[Required()])
    phone_num = TextField("phone-name")
    email = EmailField("email", validators=[Required()])
    message = TextAreaField("message")

@app.route('/contact.form', methods=["GET", "POST"])
def contact_form():
    enquiry = Enquiry()
    if enquiry.validate_on_submit():
        send_email(
            enquiry.cust_name.data,
            enquiry.email.data,
            enquiry.phone_num.data,
            enquiry.message.data
        )
        return render_template("thanks.html")
    return render_template('contact_form.html', form=enquiry )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
