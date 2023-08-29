import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
# c.execute("delete from main_sqlexplanation where step=1;")
# c.execute("select * from main_sqlexplanation")
print(c.fetchall())