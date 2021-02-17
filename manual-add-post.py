import sqlite3 as sql
from os import path
conn = sql.connect("posts.db")
c = conn.cursor()

print(path.exists("./static/arduino.jpg"))

#c.execute("CREATE TABLE POSTS (title, content, pictures)")

#c.execute("INSERT INTO POSTS VALUES (?, ?, ?)", (input("Title: "), input("Content: "), ",".join([i for i in input("Images (Seperated by ,): ").split(",") if path.exists("./static/"+i)])))

c.execute("DELETE FROM POSTS WHERE title==?", ("Code :)",))

c.execute("SELECT * FROM POSTS")
posts = [{"title": t, "content": c, "hasImages": i!='', "images": [i for i in i.split(",")]} for t, c, i in c.fetchall()]
print(posts)

c.execute("SELECT * FROM POSTS")
for i in c.fetchall():
    print(i)

conn.commit()