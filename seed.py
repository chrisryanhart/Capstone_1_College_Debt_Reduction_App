from hashlib import new
from unicodedata import name
from all_majors_seed import majors, school_majors
from models import Credential, db, School, Major, State, User, State, HouseholdIncome
from app import app

from all_majors_seed import majors, school_majors

db.drop_all()
db.create_all()

# empty table if not already empty
User.query.delete()
# Search.query.delete()
School.query.delete()
Major.query.delete()
Credential.query.delete()
State.query.delete()
# UserSearch.query.delete()

# degrees = ['Bachelors Degree', "Master's Degree", "Doctoral Degree"]
# for title in degrees:
#     degree = Degree(degree=title)
#     db.session.add(degree)

credential3 = Credential(id=3,title='Bachelors Degree')
credential5 = Credential(id=5,title="Master's Degree")
credential6 = Credential(id=6,title="Doctoral Degree")

db.session.add(credential3)
db.session.add(credential5)
db.session.add(credential6)

db.session.commit()


states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

for state in states:
    state_inst = State(name=state)
    db.session.add(state_inst)
    

db.session.commit()


# majors = ['Mechanical Engineering','Materials Engineering','Chemical Engineering']

# for title in majors:
#     major = Major(major=title)
#     db.session.add(major)

# for major in majors:
#     new_major = Major(id=major['code'], major=major['title'])
#     db.session.add(new_major)

# db.session.commit()

# major1 = Major(id="1408",major="Civil Engineering")
# major2 = Major(id="0901",major="Communication and Media Studies")
# major3 = Major(id="5203",major="Accounting and Related Services")

# db.session.add(major1)
# db.session.add(major2)
# db.session.add(major3)
# db.session.commit()


for school in school_majors:
    new_school = School(id=school['id'], name=school['school.name'])
    db.session.add(new_school)
    db.session.commit()


for major in majors:
    try:
        new_major = Major(id=major['code'], title=major['title'])
        db.session.add(new_major)
        db.session.commit()
    except:
        print('school was a duplicate')


# school1 = School(id=157085, school="University of Kentucky")
# school2 = School(id=157818, school="Transylvania University")
# school3 = School(id=157289, school="University of Louisville")
# school4 = School(id=139755, school="Georgia Institute of Technology-Main Campus")

# db.session.add(school1)
# db.session.add(school2)
# db.session.add(school3)
# db.session.add(school4)

# db.session.commit()

# degrees
# schools - should schools have their own school ID? 

# majors


