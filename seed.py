from hashlib import new
from unicodedata import name
from all_majors_seed import majors, school_majors
from models import db, SchoolMajor, TuitionType, School, Major, State, User, HouseholdIncome, SchoolMajor, ProgramFinance
from app import app


db.drop_all()
db.create_all()

# empty table if not already empty
SchoolMajor.query.delete()
TuitionType.query.delete()
HouseholdIncome.query.delete()
ProgramFinance.query.delete()
User.query.delete()
# Search.query.delete()
School.query.delete()
Major.query.delete()
# Credential.query.delete()
State.query.delete()
# UserSearch.query.delete()

# degrees = ['Bachelors Degree', "Master's Degree", "Doctoral Degree"]
# for title in degrees:
#     degree = Degree(degree=title)
#     db.session.add(degree)

# credential3 = Credential(id=3,title='Bachelors Degree')
# credential5 = Credential(id=5,title="Master's Degree")
# credential6 = Credential(id=6,title="Doctoral Degree")

# db.session.add(credential3)
# db.session.add(credential5)
# db.session.add(credential6)

# db.session.commit()


states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY','AS','GU','MP','PR','VI','MH','FM']

for state in states:
    state_inst = State(name=state)
    db.session.add(state_inst)
    
db.session.commit()

all_majors = []
duplicate_majors = []

for major in majors:
    all_majors.append(major['title'])
    try:
        new_major = Major(id=major['code'], title=major['title'])
        db.session.add(new_major)
        db.session.commit()
    except:
        print('school was a duplicate')
        duplicate_majors.append(major)

print('through major titles')

unique_major_titles = list(set(duplicate_majors))

print('extracted unique titles')
    

duplicate_schools = []
new_state=[]
major_titles = []

extracted_school_names = []
school_names = []


for school in school_majors:
    # add school state here
    try:
        state_inst = State.query.filter_by(name=school['school.state']).first()
        state_id = state_inst.id
    except:
        print('state doesnt exist')
        school_state = {'state':school['school.state'], 'name':school['school.name']}
        new_state.append(school_state)

    extracted_school_names.append(school['school.name'])
    
    try:
        new_school = School(id=str(school['id']), name=school['school.name'],state_id=state_id)
        db.session.add(new_school)
        db.session.commit()
    except:
        print('state didnt exist')

    for major in school['latest.programs.cip_4_digit']:
        new_school_major = SchoolMajor(school_id=school['id'],major_id=major['code'])
        # major['code']
        # major['title']
        db.session.add(new_school_major)
        db.session.commit()
print('finished loops')

school_names = list(set(extracted_school_names))


print('done')


# class SchoolMajor(db.Model):
#     __tablename__= "schools_majors"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     school_id = db.Column(db.String,db.ForeignKey("schools.id")) 
#     major_id = db.Column(db.String,db.ForeignKey("majors.id")) 

# school_majors[0]['school.name'] 

incomes = ["0-30000","30001-48000","48001-75000","75001-110000","110001-plus"]

for range in incomes:
    new_income = HouseholdIncome(household_income=range)
    db.session.add(new_income)
db.session.commit()

tuition_type1 = TuitionType(id=1,tuition_type='In-state')
db.session.add(tuition_type1)
db.session.commit()

tuition_type2 = TuitionType(id=2,tuition_type='Out-of-state')
db.session.add(tuition_type2)
db.session.commit()

# add 3rd type for private
tuition_type3 = TuitionType(id=3,tuition_type='Private')
db.session.add(tuition_type3)
db.session.commit()