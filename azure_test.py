import psycopg2
import os
import sys

host = os.environ['postgres_host']
dbname = os.environ['postgres_dbname']
user = os.environ['postgres_user']
password = os.environ['postgres_password']
sslmode = "require"

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")


try:
    conn = psycopg2.connect(conn_string)
    cur = con.cursor()
    cur.execute('SELECT x FROM t')
    f = open('test.sql', 'w')
    for row in cur:
        f.write("insert into t values (" + str(row) + ");")
except:
    print('Error')
    sys.exit(1)
finally:
    if con:
        con.close()



# cursor = conn.cursor()

# # Drop previous table of same name if one exists
# cursor.execute("DROP TABLE IF EXISTS inventory;")
# print("Finished dropping table (if existed)")
#
# # Create a table
# cursor.execute("CREATE TABLE person (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
# print("Finished creating table")
#
# # Insert some data into the table
# cursor.execute("INSERT INTO person (name, quantity) VALUES (%s, %s);", ("banana", 150))
# print("Inserted row of data")

# # Clean up
# conn.commit()
# cursor.close()
# conn.close()

