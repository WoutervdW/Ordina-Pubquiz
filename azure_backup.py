import psycopg2
import os
import sys

host = 'ordinapubquiz.postgres.database.azure.com'
dbname = 'postgres'
user = 'OrdinaAdmin@ordinapubquiz'
password = '@ordina123'
sslmode = "require"

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
# conn = psycopg2.connect(conn_string)


try:
    con = psycopg2.connect(conn_string)
    print("Connection established")
    cur = con.cursor()
    # Get all tables and loop over them to write the backup sql
    tables = ["team"]
    # tables = ["team", "person", "question", "type", "category"]
    # cur.execute("""Select table_name FROM information_schema.tables WHERE table_schema = 'public'""")
    for table in tables:
        print(table)
        # Loop over the column names, we use this to construct the insert statement
        cur.execute("Select * from " + table + " LIMIT 0")
        backupline = "insert into " + table + " ("
        for column in cur.description:
            print(column[0])
            backupline += column[0] +", "
        # We remove the final 2 character to remove the obsolete comma
        backupline = backupline[:-2]
        backupline += ") values ( %s, %s, %s);"
        cur.execute("select * from " + table)
        f = open('backup_azure.sql', 'w')
        for row in cur:
            f.write(backupline % row)
            f.write('\n')
        f.close()

        # Create the backup line, we assume the tables are created properly
    # f = open('test.sql', 'w')
    # for row in cur:
    #     f.write("insert into t values (" + str(row) + ");")
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

