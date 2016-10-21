import csv

rows = []
with open('population.csv','rb') as f:
    [ rows.append(row) for row in csv.reader(f) ]

def utf8(s):
    return s.decode('utf-8')

population = []

districts = []
for r in rows[1:]:
    district = District(utf8(r[0]))
    districts.append(district)
    pps.append(Population(year=r[7],
                          district=district,
                          men=r[1],
                          women=r[2],
                          children=r[3],
                          employable_men=r[4],
                          employable_women=r[5]))

[ db.session.add(d) for d in districts ]
[ db.session.add(p) for p in population ]
db.session.commit()

with open('hospitals.csv','rb') as f:
    [ rows.append(row) for row in csv.reader(f) ]

hospitals =  []
diseases = []
for h in rows[:1]:

    hospital = Hospital(name=utf8(r[0]),
            district=Distict.name.like('%{}%'.format(utf8(r[7]))))
    hospitals.append(hospital)

    diseases.append(Disease(name=utf8(r[6]),
                           hospital=hospital,
                           adults=r[1],
                           adults_observed=r[2],
                           children=r[3],
                           children_observed=r[4],
                           year=r[5]))

[ db.session.add(h) for h in hospitals ]
[ db.session.add(d) for d in diseases ]
db.session.commit()


#l =[ District(name=row.decode('utf-8')) for row in rows[1:] if row ]

#[db.session.add(d) for d in l ]
#db.session.commit()


