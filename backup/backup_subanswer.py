

def backup_subanswer(f, cur):
    table = "subanswer"
    print(table)
    # Loop over the column names, we use this to construct the insert statement
    cur.execute("Select * from " + table + " LIMIT 0")
    backupline = "insert into " + table + " ("
    for column in cur.description:
        backupline += column[0] + ", "
    # We remove the final 2 character to remove the obsolete comma
    backupline = backupline[:-2]
    backupline += ") values ( %s, %s);"
    print(backupline)
    cur.execute("select * from " + table)
    for row in cur:
        final = []
        print(row)
        final.append(str(row[0]))
        final.append(str(row[1]))
        result = backupline % (final[0], final[1])
        f.write(result)
        f.write('\n')

