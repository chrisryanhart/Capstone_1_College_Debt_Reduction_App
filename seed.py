from hashlib import new
from unicodedata import name
from all_majors_seed import majors, school_majors
from models import db, SchoolMajor, TuitionType, School, Major, State, User, HouseholdIncome, SchoolMajor, ProgramFinance
from app import app


db.drop_all()
db.create_all()

SchoolMajor.query.delete()
TuitionType.query.delete()
HouseholdIncome.query.delete()
ProgramFinance.query.delete()
User.query.delete()
School.query.delete()
Major.query.delete()
State.query.delete()


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
all_major_codes = []

for major in majors:
    if major['title'] not in all_majors:
        all_majors.append(major['title'])
        all_major_codes.append(major['code'])
        new_major = Major(id=major['code'], title=major['title'])
        db.session.add(new_major)
        db.session.commit()
    else:
        print('major was duplicate')

    
duplicate_schools = []
new_state=[]
major_titles = []

extracted_school_names = []
school_names = []
school_not_added = []


for school in school_majors:
    duplicate_name_check = School.query.filter_by(name=school['school.name']).first()
    state_inst = State.query.filter_by(name=school['school.state']).first()

    # if a school isn't a duplicate, add the school
    if not duplicate_name_check:
        new_school = School(id=str(school['id']), name=school['school.name'],state_id=state_inst.id)
        db.session.add(new_school)
        db.session.commit()
                
        # if the major exists in the db, add the school's majors
        for major in school['latest.programs.cip_4_digit']:
            if major['code'] in all_major_codes:
                new_school_major = SchoolMajor(school_id=school['id'],major_id=major['code'])
                db.session.add(new_school_major)
                db.session.commit()

    # confirm the school isn't a duplicate
    elif duplicate_name_check and duplicate_name_check.state_id != state_inst.id:
        new_school = School(id=str(school['id']), name=school['school.name'],state_id=state_inst.id)
        db.session.add(new_school)
        db.session.commit()

        for major in school['latest.programs.cip_4_digit']:
            if major['code'] in all_major_codes:
                new_school_major = SchoolMajor(school_id=school['id'],major_id=major['code'])
                db.session.add(new_school_major)
                db.session.commit()

    else:
        'dont add school'
        school_info = {'code':school['id'] , 'name':school['school.name'] }
        school_not_added.append(school_info)
        


school_names = list(set(extracted_school_names))



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

tuition_type3 = TuitionType(id=3,tuition_type='Private')
db.session.add(tuition_type3)
db.session.commit()