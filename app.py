import os
from flask import Flask, session
from flask import render_template
from flask.globals import request
from flaskext.sqlalchemy import SQLAlchemy
from logbook import debug
from werkzeug.utils import redirect, secure_filename
from orm import orm, ContentItem, Postcard, Image

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# sqlalchemy config:
from config import conn_url, upload_path

app.config['SQLALCHEMY_DATABASE_URI'] = conn_url
app.config['UPLOAD_FOLDER'] = upload_path
orm.init_app(app)

from orm import ContentItem

# database management pages
from admin import sysadmin_pages
app.register_blueprint(sysadmin_pages)

# authentication pages
from authentication import authweb, requires_login
app.register_blueprint(authweb)

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

ext_allowed = tuple('jpg jpe jpeg png gif svg bmp'.split())

def allowed(filename):
    return (extension(filename) in ext_allowed)

def extension(filename):
    return filename.rsplit('.', 1)[-1]

@app.route('/postcard/add', methods=['POST'])
@requires_login
def postcard_add():
    user=session.get("user") # i wonder if there is a neater way of doing this?
    # log any parameters passed in and any other state
    action="create_postcard"
    debug("action={} user={}", action, user)
    #
    file = request.files['file']
    debug(file)
    filename = secure_filename(file.filename)
    if allowed(filename):
        pathname = os.path.join( app.config["UPLOAD_FOLDER"], filename)
        file.save( pathname )
        postcard = Postcard( user, Image(filename), "yo bliar" )
        postcard.save()
        return redirect('/postcards')
    else:
        return "Invalid file type"

if __name__ == '__main__':
    app.run(debug=True)
