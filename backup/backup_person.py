
def backup_person(f, cur):
    table = "person"
    print(table)
    # Loop over the column names, we use this to construct the insert statement
    cur.execute("Select * from " + table + " LIMIT 0")
    backupline = "insert into " + table + " ("
    for column in cur.description:
        backupline += column[0] + ", "
    # We remove the final 2 character to remove the obsolete comma
    backupline = backupline[:-2]
    backupline += ") values ( %s, %s, %s);"
    print(backupline)
    cur.execute("select * from " + table)
    for row in cur:
        final = [str(row[0]), '\'' + str(row[1] + '\''), '\'' + str(row[2] + '\'')]
        print(row)
        result = backupline % (final[0], final[1], final[2])
        print(result)
        f.write(result)
        f.write('\n')

