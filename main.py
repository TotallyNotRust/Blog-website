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

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

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
 
def getPosts(ID = None):
    conn = sql.connect("posts.db")
    c = conn.cursor()
    if ID:
        c.execute("SELECT * FROM POSTS WHERE id==?", (int(ID), ))
    else:
        c.execute("SELECT * FROM POSTS")
    print(ID)
    posts = [{"title": t, "content": c, "images": ["\static\\"+i for i in i.split(",") if i!=''], "id": I} for t, c, i, I in c.fetchall()]
    return posts

def submitPost(title, body, picture):
    conn = sql.connect("posts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts")
    c.execute("INSERT INTO POSTS VALUES (?, ?, ?, ?)", (title, body, picture, len(c.fetchall())))
    conn.commit()

@app.route("/removeKey")
def removeKey():
    resp = redirect(url_for('mainPage'))
    resp.set_cookie('key', '')
    return resp

@app.route("/editPost", methods=['GET', 'POST'])
def editPost():
    if request.cookies.get("key") == hashlib.md5((key+request.remote_addr).encode()).hexdigest():
        form = MakePost()
        conn = sql.connect("posts.db")
        c = conn.cursor()
        if form.validate_on_submit():
            ID = request.args.get("id")
            
            if form.pictures.data:
                picture = save_image(form.pictures.data)
            else:
                picture = ""
            flash('Post made.', 'success')
            c.execute("UPDATE posts SET title=?, content=?, pictures=? WHERE id==?", (form.title.data, form.body.data, picture, int(ID),))
            conn.commit() 
            return redirect(url_for('mainPage'))
        else:
            Post = getPosts(request.args.get("id"))[0]
            form.title.data, form.body.data, picture, ID = Post["title"],Post["content"],Post["images"],Post["id"]
            return render_template("makePost.html", title="Make post", form=form)
    else:
        return page_not_found('')

@app.route("/post")
def fullPost():
    form = MakePost()
    conn = sql.connect("posts.db")
    c = conn.cursor()
    post = getPosts(request.args.get("id"))[0]
    code = {str(post["id"]): post["content"].split("``")[1::2]}
    post = post | {"content":"--code".join(post["content"].split("``")[::2])} 
    return render_template("fullPagePost.html", title="Make post", post=post, code=code)

@app.route("/delete")
def deletePost():
    if request.cookies.get("key") == hashlib.md5((key+request.remote_addr).encode()).hexdigest():
        ID = request.args.get("id")
        conn = sql.connect("posts.db")
        c = conn.cursor()
        c.execute("DELETE FROM posts WHERE id==?", (int(ID),))
        conn.commit()
        c.execute("SELECT * FROM posts")
        for indent, i in enumerate(c.fetchall()):
            print(i[3], ":", str(indent))
            c.execute("UPDATE posts SET id=? WHERE id==?", (indent, i[3]))
        conn.commit()
        return redirect(url_for('mainPage'))
    else:
        return page_not_found('')

@app.route("/")
def mainPage():
    [print(f'{i}: {request.cookies.get(i)}') for i in request.cookies]
    if not request.cookies.get('seenCookies') == "1":
        flash("This site uses cookies to keep track of users, none of this data is stored or sold.")
    posts = getPosts()
    print(posts)

    code = {str(i["id"]): i["content"].split("``")[1::2] for i in posts}
    
    #print([{"content":"--code".join(i["content"].split("``")[::2])} for i in posts])
    posts = [i | {"content":"--code".join(i["content"].split("``")[::2])} for i in posts]
    print(code)
    #print(code["1"])
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

@app.route("/about")
def aboutPage():
    image = os.path.join(app.root_path, 'static\\', "aboutMe.jpg")
    isAdmin=request.cookies.get('key')==hashlib.md5((key+request.remote_addr).encode()).hexdigest()
    return make_response(render_template("aboutPage.html", isAdmin=isAdmin, image=image))
@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Page not found</h1>'

if __name__ == "__main__":
    while True:
        try:
            app.run(debug=True)
        except:
            pass