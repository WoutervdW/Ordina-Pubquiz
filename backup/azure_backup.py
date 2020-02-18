import psycopg2
import sys
from backup import backup_team
from backup import backup_person
from backup import backup_category
from backup import backup_question
from backup import backup_type
from backup import backup_subanswer
from backup import backup_variant

# Take host information from .flaskenv and paste it here.
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
    f = open('backup/backup_azure.txt', 'w')
    # We will backup the database in a custom manner. We don't want any image file,
    # just what's important to start the quiz.
    print("first backup person")
    backup_person.backup_person(f, cur)
    print('backup teams')
    backup_team.backup_team(f, cur)
    print("backup category")
    backup_category.backup_category(f, cur)
    print("backup type")
    backup_type.backup_type(f, cur)
    print("backup questions, we should have backupped all the necessary information")
    backup_question.backup_questions(f, cur)
    print("backup the correct answers for the questions, or subanswer and after variants")
    backup_subanswer.backup_subanswer(f, cur)
    print("backup variant")
    backup_variant.backup_variant(f, cur)
    f.close()


except:
    print('Error')
    sys.exit(1)
finally:
    if con:
        con.close()

