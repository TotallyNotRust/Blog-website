from flask import Flask, render_template, flash, redirect, url_for, request, make_response, send_file
import sqlite3 as sql
import sys, secrets, logging, hashlib, os
from makeNewPost import MakePost
from datetime import datetime
from login import Login
import markdown
from flask_pretty import Prettify

print(logging.DEBUG)
logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)

app = Flask(__name__)

if any([i.startswith('rS') or i.startswith('randomString') for i in sys.argv]):
    key = secrets.token_hex(16)
    app.config['SECRET_KEY'] = secrets.token_hex(16)
else:
    key = 'dad2e006454f0064098c2f6a65487df3'
    app.config['SECRET_KEY'] = '9f4a6d5b560f3e4e03589b625aabf209'

password = "admin"

UPLOAD_FOLDER = os.path.join('static')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print(key)
print(app.config['SECRET_KEY'])
 
def getPosts():

    conn = sql.connect("posts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM POSTS")
    posts = [{"title": t, "content": c, "images": ["\static\\"+i for i in i.split(",") if i!='']} for t, c, i in c.fetchall()]
    return posts

def submitPost(title, body, picture):
    conn = sql.connect("posts.db")
    c = conn.cursor()
    c.execute("INSERT INTO POSTS VALUES (?, ?, ?)", (title, body, picture))
    conn.commit()

@app.route("/removeKey")
def removeKey():
    resp = redirect(url_for('mainPage'))
    resp.set_cookie('key', '')
    return resp

@app.route("/")
def mainPage():

    [print(f'{i}: {request.cookies.get(i)}') for i in request.cookies]
    if not request.cookies.get('seenCookies') == "1":
        flash("This site uses cookies to keep track of users, none of this data is stored or sold.")
    posts = getPosts()
    print(posts)

    code = [i["content"].split("``")[1::2] for i in posts]
    
    print([{"content":"--code".join(i["content"].split("``")[::2])} for i in posts])
    posts = [i | {"content":"--code".join(i["content"].split("``")[::2])} for i in posts]

    resp = make_response(render_template("html.html", title="Gustav's blog", posts=posts, code=code, isAdmin=request.cookies.get('key')==hashlib.md5((key+request.remote_addr).encode()).hexdigest()))
    resp.set_cookie('seenCookies', "1")
    return resp

def save_image(image):
    name = hashlib.md5(datetime.now().strftime("%Y%d%m%M%H%S").encode()).hexdigest()
    _, ext = os.path.splitext(image.filename)
    path = os.path.join(app.root_path, 'static\\', name+ext)
    image.save(path)
    return name+ext

@app.route("/makePost", methods=['GET', 'POST'])
def makePost():
    print(request.cookies.get("key"))
    print(hashlib.md5((key+request.remote_addr).encode()).hexdigest())
    if request.cookies.get("key") == hashlib.md5((key+request.remote_addr).encode()).hexdigest():
        form = MakePost()
        if form.validate_on_submit():
            if form.pictures.data:
                picture = save_image(form.pictures.data)
            else:
                picture = ""
            flash('Post made.', 'success')
            submitPost(form.title.data, form.body.data, picture)
            print(f'{datetime.now()}: Post made by {request.remote_addr}, with the title: {form.title.data}') 
            return redirect(url_for('mainPage'))
        else:
            return render_template("makePost.html", title="Make post", form=form)
    else:
        return page_not_found('')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        if form.password.data == password:
            resp = redirect(url_for('mainPage'))
            resp.set_cookie('key', hashlib.md5((key+request.remote_addr).encode()).hexdigest())
            logging.warning(f'{datetime.now()}:{request.remote_addr} logged in')
            return resp
        else:
            flash('Incorrect password')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Page not found</h1>'

if __name__ == "__main__":
    while True:
        try:
            app.run(debug=True)
        except:
            pass