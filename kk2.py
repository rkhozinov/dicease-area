import csv

rows = []
with open('districts.csv','rb') as f:
    [ rows.append(row[0]) for row in csv.reader(f) ]

l =[ District(name=row.decode('utf-8')) for row in rows[1:] if row ]

db.session.add_all(l)
db.session.commit()
