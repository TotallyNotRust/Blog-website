import sqlite3 as sql
from os import path
conn = sql.connect("posts.db")
c = conn.cursor()

print(path.exists("./static/arduino.jpg"))

c.execute("CREATE TABLE POSTS (title, content, pictures, id)")

#c.execute("INSERT INTO POSTS VALUES (?, ?, ?)", (input("Title: "), input("Content: "), ",".join([i for i in input("Images (Seperated by ,): ").split(",") if path.exists("./static/"+i)])))

#c.execute("DELETE FROM POSTS WHERE title==?", ("Code :)",))
def getPost():
    c.execute("SELECT * FROM POSTS")
    posts = [{"title": t, "content": c, "hasImages": i!='', "images": [i for i in i.split(",")], "id": I} for t, c, i, I in c.fetchall()]
    print(posts)

getPost()

c.execute("UPDATE posts SET id=? WHERE id==?", ("0", "1"))

getPost()

conn.commit()