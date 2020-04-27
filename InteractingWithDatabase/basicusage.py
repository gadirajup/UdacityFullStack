import psycopg2 as pg

connection = pg.connect('dbname=test')

cursor = connection.cursor()

cursor.execute(
    'DROP TABLE IF EXISTS table2'
)

cursor.execute('''
CREATE TABLE table2 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
);
''')

cursor.execute(f'''
INSERT INTO table2 (
    id, completed) 
VALUES (
    {5}, {True});
''')

cursor.execute('SELECT * FROM table2;')

results = cursor.fetchAll()
print(results)

connection.commit()
connection.close()
cursor.close()
