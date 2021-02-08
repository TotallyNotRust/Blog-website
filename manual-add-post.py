import sqlite3 as sql
conn = sql.connect("posts.db")
c = conn.cursor()

#c.execute("CREATE TABLE POSTS (title, content)")

#c.execute("INSERT INTO POSTS VALUES (?, ?)", (input("Title: "), input("Content: ")))

c.execute("SELECT * FROM POSTS")
for i in c.fetchall():
    print(i)

conn.commit()