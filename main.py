from flask import Flask, render_template, flash, redirect, url_for
import sqlite3 as sql
from makeNewPost import MakePost

app = Flask(__name__)


app.config['SECRET_KEY'] = '9f4a6d5b560f3e4e03589b625aabf209'
 
def getPosts():
    conn = sql.connect("posts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM POSTS")
    posts = [{"title": t, "content": c} for t, c in c.fetchall()]

    return posts

def submitPost(title, body):
    conn = sql.connect("posts.db")
    c = conn.cursor()
    c.execute("INSERT INTO POSTS VALUES (?, ?)", (title, body))
    conn.commit()

@app.route("/")
def mainPage():
    posts = getPosts()
    print(posts)
    return render_template("html.html", title="Gustav's blog", posts=posts)

@app.route("/makePost", methods=['GET', 'POST'])
def makePost():
    form = MakePost()
    if form.validate_on_submit():
        flash('Post made.', 'success')
        print("Worked")
        submitPost(form.title.data, form.body.data)
        return redirect(url_for('mainPage'))
    else:
        print("Ditnt work")
    return render_template("makePost.html", title="Make post", form=form)

if __name__ == "__main__":
    app.run(debug=True)