

def backup_type(f, cur):
    table = "type"
    print(table)
    # Loop over the column names, we use this to construct the insert statement
    cur.execute("Select * from " + table + " LIMIT 0")
    backupline = "insert into " + table + " ("
    for column in cur.description:
        backupline += column[0] + ", "
    # We remove the final 2 character to remove the obsolete comma
    backupline = backupline[:-2]
    backupline += ") values ( %s, %s);"
    cur.execute("select * from " + table)
    for row in cur:
        final = []
        print(row)
        final.append(str(row[0]))
        # We know that the second entry is the name, this should be encapsulated in string comma's ('')
        final.append('\'' + row[1] + '\'')
        # Not sure why, but we can finnaly get the query using this work around
        result = backupline % (final[0], final[1])
        f.write(result)
        f.write('\n')

