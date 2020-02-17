
def backup_questions(f, cur):
    table = "question"
    print(table)
    # Loop over the column names, we use this to construct the insert statement
    cur.execute("Select * from " + table + " LIMIT 0")
    backupline = "insert into " + table + " ("
    for column in cur.description:
        backupline += column[0] + ", "
    # We remove the final 2 character to remove the obsolete comma
    backupline = backupline[:-2]
    backupline += ") values ( %s, %s, %s, %s, %s, %s, %s);"
    print(backupline)
    cur.execute("select * from " + table)
    for row in cur:
        final = []
        print(row)
        final.append(str(row[0]))
        final.append(str(row[1]))
        final.append(str(row[2]))
        final.append(str(row[3]))
        if row[4] is None:
            final.append("Null")
        else:
            final.append(str(row[4]))
        final.append('\'' + row[5] + '\'')
        if row[6] is None:
            final.append("Null")
        else:
            final.append(str(row[6]))
        # Not sure why, but we can finnaly get the query using this work around
        result = backupline % (final[0], final[1], final[2], final[3], final[4], final[5], final[6])
        f.write(result)
        f.write('\n')

