import psycopg2
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
    with open('backup/backup_azure.txt', 'r') as f:
        for line in f:
            line = line.strip()
            print(line)
            cur.execute(line)
            print("executed " + line)
except:
    print('Error')
    sys.exit(1)
finally:
    con.commit()
    cur.close()
    con.close()
    if con:
        con.close()
