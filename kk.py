# coding: utf-8
import csv

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

rows = []
with open('districts.csv','rb') as f:
    [ rows.append(row) for row in unicode_csv_reader(f) ]

[ District(name=row) for row in rows[1:]]
l =[ District(name=row) for row in rows[1:]]
type(l[0])

l =[ District(name=row[0]) for row in rows[1:] if row ]

for d in l:
    print d
