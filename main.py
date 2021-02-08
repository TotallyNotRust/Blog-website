from flask import Flask, render_template
import sqlite3 as sql

app = Flask(__name__)


posts = [
    {
        "title": "Circus story",
        "content": "Today i went to the circus",
    },
    {
        "title": "Zoo story",
        "content": "Today i went to the zoo",
    }
]

def getPosts():
    conn = sql.connect("posts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM POSTS")
    posts = [{"title": t, "content": c} for t, c in c.fetchall()]

    return posts

@app.route("/")
def main():
    print(posts)
    return render_template("html.html", posts=getPosts())

if __name__ == "__main__":
    app.run(debug=True)