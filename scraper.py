#!/bin/python3
from hashlib import new
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
from googlesearch import search
import datetime
import mysql.connector
import xlsxwriter
import os
from config import host, database, myuser, mypass, badwords


# MySQL Connector

myconn = mysql.connector.connect(host=host, database=database, user=myuser, password=mypass)

gquery = input('[+] Search Term: ')
uTotalSearch = input('[+] Number Of URL Results: ')
uTotalScan = input('[+] Number Of Pages To Scan: ')
gtotal = int(uTotalSearch)
gurls = []
for j in search(gquery, tld="com", num=int(gtotal), stop=int(gtotal), pause=2):
    gurls.append(j)
print('Collecting URLs')
print('-' * 80)
g_count = 0

for k in gurls:
    g_count += 1
    print('[' + str(g_count) + '] ' + k)
user_total = int(uTotalScan)
scrapped_urls = set()
emails = set()
count = 0

for user_urls in gurls:
    urls = deque([user_urls])
    print('-' * 80)
    try:
        while len(urls):
            if count == int(user_total):
                count = 0
                break
            
            count += 1
            url = urls.popleft()
            scrapped_urls.add(url)
            parts =  urllib.parse.urlsplit(url)
            base_url = '{0.scheme}://{0.netloc}'.format(parts)
            path = url[:url.rfind('/')+1] if '/' in parts.path else url
            print('[%d] Processing %s' % (count,url))
            
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue
            
            new_emails = set(re.findall(r'[a-z0-9\.\-+]+@[a-z0-9\.\-+]+\.[a-z]+', response.text, re.I))
            emails.update(new_emails)

            for l in emails:
                NULL_ = None
                date_time = datetime.datetime.now()
                _date = str(date_time.date())
                _time = str(date_time.strftime("%X"))
                cursor = myconn.cursor(buffered=True)
                emailBulk = (NULL_, gquery, l, _date, _time)
                sql = "INSERT INTO `emailbulk`(`ID`,`searchterm`,`email`,`date`,`time`) VALUES(%s,%s,%s,%s,%s)"
                cursor.execute(sql,emailBulk)
                myconn.commit()
            
            soup = BeautifulSoup(response.text, features='lxml')
            
            for anchor in soup.find_all('a'):
                link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                if not link in urls and not link in scrapped_urls:
                    urls.append(link)
    except KeyboardInterrupt:
        count = 0
        print('[-] Closing"')
print('-' * 80)
for mail in emails:
    print(mail)
    NULL_ = None
    date_time = datetime.datetime.now()
    _date = str(date_time.date())
    _time = str(date_time.strftime("%X"))
    cursor = myconn.cursor(buffered=True)
    emailsScrapped = (NULL_, gquery, mail, _date, _time)
    sql = "INSERT INTO `emails`(`ID`,`searchterm`,`email`,`date`,`time`) VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(sql,emailsScrapped)
    myconn.commit()

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

print('-' * 80)
totalemails = len(emails) - noDel
lenemails = len(emails)
print(f'Collected: {lenemails} Emails!')
print(f'Deleted: {noDel} Invalid Emails!')
print(f'Total: {totalemails} Valid Emails!' )

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(f'./xls/{gquery}.xlsx')
worksheet = workbook.add_worksheet()

sqlemails = "SELECT searchterm, email From emails Where searchterm = '" + gquery + "' Group By email Order By email Asc"
cursor.execute(sqlemails)
result = cursor.fetchall()

row = 0
col = 0

for i in result:
    term = i[0]
    mail = i[1]
    worksheet.write(row, col,     i[0])
    worksheet.write(row, col + 1, i[1])
    row += 1   

worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, row)
print('-' * 80)
print(f'{row} Emails Imported to {os.getcwd()}/xls/{gquery}.xlsx')
print('-' * 80)
workbook.close()