import psycopg2 as pg

connection = pg.connect('dbname=test')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS table3;')

cursor.execute('''
CREATE TABLE table3 (
    id INTEGER PRIMARY KEY,
    taskname VARCHAR NOT NULL
);
''')

cursor.execute(f'''
INSERT INTO table3 (
    id, taskname) 
VALUES (
    {5}, {'True'});
''')

cursor.execute(
    'SELECT * FROM table3;'
)

results = cursor.fetchAll()
print(results)

connection.commit()

cursor.close()
connection.close()
