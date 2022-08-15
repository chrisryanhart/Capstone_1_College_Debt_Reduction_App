from models import db, Search, School, Major, Degree, State, UserSearch, User
from app import app

db.drop_all()
db.create_all()

# empty table if not already empty
User.query.delete()
Search.query.delete()
School.query.delete()
Major.query.delete()
Degree.query.delete()
State.query.delete()
UserSearch.query.delete()

degrees = ['Bachelors Degree', "Master's Degree", "Doctoral Degree"]
for title in degrees:
    degree = Degree(degree=title)
    db.session.add(degree)

db.session.commit()


states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

for state in states:
    state_inst = State(state=state)
    db.session.add(state_inst)

db.session.commit()


majors = ['Mechanical Engineering','Materials Engineering','Chemical Engineering']

for title in majors:
    major = Major(major=title)
    db.session.add(major)

db.session.commit()


school1 = School(id=157085, school="University of Kentucky")
school2 = School(id=157818, school="Transylvania University")
school3 = School(id=157289, school="University of Louisville")
school4 = School(id=139755, school="Georgia Institute of Technology-Main Campus")

db.session.add(school1)
db.session.add(school2)
db.session.add(school3)
db.session.add(school4)

db.session.commit()

# degrees
# schools - should schools have their own school ID? 

# majors


