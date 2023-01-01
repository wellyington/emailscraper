import mysql.connector
from config import host, database, myuser, mypass, badwords

# MySQL Connector
myconn = mysql.connector.connect(host=host, database=database, user=myuser, password=mypass)

noDel = 0
for badword in badwords:

    check = badword

    cursor = myconn.cursor(buffered=True)
    sqlAdd = "select id, email From emails where email like '%" + check + "%'"
    cursor.execute(sqlAdd)
    toDelete = cursor.fetchall()
    for tdel in toDelete:
        print(str(tdel[0]) + " : " + tdel[1])
        sqlDelete = "DELETE FROM emails WHERE id = " + str(tdel[0])
        cursor.execute(sqlDelete)
        myconn.commit()
        noDel += 1

print('-' * 50)
print(f'Deleted {noDel} Bad Emails!')
print('-' * 50)