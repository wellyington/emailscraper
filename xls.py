import xlsxwriter
import mysql.connector
from config import host, database, myuser, mypass, badwords

searchterm = input('Search Term: ')

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(f'./xls/{searchterm}.xlsx')
worksheet = workbook.add_worksheet()

# MySQL Connector
myconn = mysql.connector.connect(host=host, database=database, user=myuser, password=mypass)
cursor = myconn.cursor(buffered=True)
sqlemails = "SELECT searchterm, email From emails Where searchterm = '" + searchterm + "' Group By email Order By email Asc"
cursor.execute(sqlemails)
result = cursor.fetchall()

maillist = []

row = 0
col = 0

for i in result:
    term = i[0]
    mail = i[1]
    print(f'{term} - {mail} Imported to XLSX File.')
    worksheet.write(row, col,     i[0])
    worksheet.write(row, col + 1, i[1])
    row += 1   

worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, row)
print('-' * 50)
print(f'{row} Emails Imported to XLSX FIle.')
print('-' * 50)
workbook.close()