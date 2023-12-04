#!/bin/python3
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
from googlesearch import search
import datetime
import sqlite3
import xlsxwriter
import os
from config import badwords

# Create a SQLite database connection
conn = sqlite3.connect('emails.db')
cursor = conn.cursor()

# Create the emails table
cursor.execute('''
CREATE TABLE IF NOT EXISTS emails (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    searchterm TEXT,
    email TEXT,
    date TEXT,
    time TEXT
)
''')
g_count = 0
gquery = input('[+] Search Term: ')
uTotalSearch = input('[+] Number Of URL Results: ')
uTotalScan = input('[+] Number Of Pages To Scan: ')
gtotal = int(uTotalSearch)
gurls = []

# Create a workbook and add a worksheet
workbook = xlsxwriter.Workbook(f'./xls/{gquery}.xlsx')
worksheet = workbook.add_worksheet()

for j in search(gquery, tld="com", num=int(gtotal), stop=int(gtotal), pause=2):
    gurls.append(j)

print('Collecting URLs')
print('-' * 80)

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
            parts = urllib.parse.urlsplit(url)
            base_url = '{0.scheme}://{0.netloc}'.format(parts)
            path = url[:url.rfind('/') + 1] if '/' in parts.path else url
            print('[%d] Processing %s' % (count, url))

            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

            new_emails = set(re.findall(r'[a-z0-9\.\-+]+@[a-z0-9\.\-+]+\.[a-z]+', response.text, re.I))
            emails.update(new_emails)

            for l in emails:
                date_time = datetime.datetime.now()
                _date = str(date_time.date())
                _time = str(date_time.strftime("%X"))
                emailBulk = (gquery, l, _date, _time)
                cursor.execute("INSERT INTO emails (searchterm, email, date, time) VALUES (?, ?, ?, ?)", emailBulk)
                conn.commit()

            soup = BeautifulSoup(response.text, features='lxml')

            for anchor in soup.find_all('a'):
                link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                if link not in urls and link not in scrapped_urls:
                    urls.append(link)
    except KeyboardInterrupt:
        count = 0
        print('[-] Closing')

print('-' * 80)
for mail in emails:
    print(mail)
    date_time = datetime.datetime.now()
    _date = str(date_time.date())
    _time = str(date_time.strftime("%X"))
    emailsScrapped = (gquery, mail, _date, _time)
    cursor.execute("INSERT INTO emails (searchterm, email, date, time) VALUES (?, ?, ?, ?)", emailsScrapped)
    conn.commit()

noDel = 0
for badword in badwords:
    check = badword
    sqlAdd = f"SELECT ID, email FROM emails WHERE email LIKE '%{check}%'"
    cursor.execute(sqlAdd)
    toDelete = cursor.fetchall()
    for tdel in toDelete:
        print(f"{tdel[0]} : {tdel[1]}")
        sqlDelete = f"DELETE FROM emails WHERE ID = {tdel[0]}"
        cursor.execute(sqlDelete)
        conn.commit()
        noDel += 1

print('-' * 80)
totalemails = len(emails) - noDel
lenemails = len(emails)
print(f'Collected: {lenemails} Emails!')
print(f'Deleted: {noDel} Invalid Emails!')
print(f'Total: {totalemails} Valid Emails!')

sqlemails = f"SELECT searchterm, email FROM emails WHERE searchterm = '{gquery}' GROUP BY email ORDER BY email ASC"
cursor.execute(sqlemails)
result = cursor.fetchall()

row = 0
col = 0

for i in result:
    term = i[0]
    mail = i[1]
    worksheet.write(row, col, i[0])
    worksheet.write(row, col + 1, i[1])
    row += 1

worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, row)
print('-' * 80)
print(f'{row} Emails Imported to {os.getcwd()}/xls/{gquery}.xlsx')
print('-' * 80)
workbook.close()
conn.close()
os.remove("emails.db")