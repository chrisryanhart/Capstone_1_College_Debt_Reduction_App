from app import *

def call_college_API(school_id,major_id,school_state,household_income,home_state,degree_id,data):

    payload = {"id": f"{school_id}","school.state": f"{school_state}", "_fields": "id,school.name,latest.cost,latest.school.ownership,latest.school.state", "api_key": f"{API_key}"}

    cost_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json', params=payload)

    cost_data = cost_resp.json()

    # Determine if school is public in-state, public out-of-state, or private
    ownership = cost_data['results'][0]['latest.school.ownership']

    # verify tuition is out of state and public

    data = verify_tuition_type(ownership,home_state,school_state,data, household_income,cost_data)
    
    # make API call for earnings data
    major_params = {
            'id':f'{school_id}','latest.programs.cip_4_digit.credential.level':f"{degree_id}", 'latest.programs.cip_4_digit.code':f"{major_id}", 
            '_fields':'id,school.name,latest.programs.cip_4_digit.earnings.highest.1_yr.overall_median_earnings,latest.programs.cip_4_digit.earnings.highest.2_yr.overall_median_earnings,latest.programs.cip_4_digit.earnings.highest.3_yr.overall_median_earnings',
            "api_key": f"{API_key}"
            }

    earnings_resp = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json', major_params)
    earnings_data = earnings_resp.json()

    # extract earnings data from API resp
    yr_1_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['1_yr']['overall_median_earnings']
    yr_2_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['2_yr']['overall_median_earnings']
    yr_3_earnings = earnings_data['results'][0]['latest.programs.cip_4_digit'][0]['earnings']['highest']['3_yr']['overall_median_earnings']

    yr_1_earnings = convert_to_currency_format(yr_1_earnings)
    yr_2_earnings = convert_to_currency_format(yr_2_earnings)
    yr_3_earnings = convert_to_currency_format(yr_3_earnings)

    data['yr_1_earnings'] = yr_1_earnings
    data['yr_2_earnings'] = yr_2_earnings
    data['yr_3_earnings'] = yr_3_earnings

    return data

def convert_to_currency_format(earnings_amt):
    if not earnings_amt or earnings_amt < 0:
        earnings_amt = 'No data'
    else:
        earnings_amt = "${:0,}".format(earnings_amt) 
    return earnings_amt

def verify_tuition_type(ownership,home_state,school_state,data,household_income,cost_data):
    if home_state != school_state and ownership == 1:
        out_of_state_tuition = cost_data['results'][0]['latest.cost.tuition.out_of_state']
        books = cost_data['results'][0]['latest.cost.booksupply']
        roomboard = cost_data['results'][0]['latest.cost.roomboard.oncampus']
        misc_expense = cost_data['results'][0]['latest.cost.otherexpense.oncampus']
            
        total_out_of_state_cost = out_of_state_tuition + roomboard + books + misc_expense

        if not total_out_of_state_cost or total_out_of_state_cost < 0:
                total_out_of_state_cost = 'No data'
        else:
            total_out_of_state_cost = "${:0,}".format(total_out_of_state_cost) 

            data['tuition'] = total_out_of_state_cost
            data['tuition_type'] = 'Out-of-state'
       
    # Verify school is private (not public)
    if ownership != 1:
        private_net_cost = cost_data['results'][0][f'latest.cost.net_price.private.by_income_level.{household_income}']

        if not private_net_cost or private_net_cost < 0:
            private_net_cost = 'No data'
        else:
            private_net_cost = "${:0,}".format(private_net_cost) 

        data['tuition'] = private_net_cost
        data['tuition_type'] = 'Private'
        
    # Check if school is considered in-state
    if home_state == school_state and ownership == 1:
        net_in_state_public_cost = cost_data['results'][0][f'latest.cost.net_price.public.by_income_level.{household_income}']
            
        if not net_in_state_public_cost or net_in_state_public_cost < 0:
            net_in_state_public_cost = 'No data'
        else:
            net_in_state_public_cost = "${:0,}".format(net_in_state_public_cost) 
            
        data['tuition'] = net_in_state_public_cost
        data['tuition_type'] = 'In-state'
    return data

def retrieve_program_finances(program_finances):
    data = []

    for program_finance in program_finances:
        program_finance_data = {}
        
        program_finance_data['school_name'] = program_finance.schools.name
        program_finance_data['major_name'] = program_finance.majors.title
        program_finance_data['credential_title'] = 'Bachelors Degree'
        program_finance_data['school_state'] = program_finance.schools.states.name
     
        # program_finance_inst = ProgramFinance.query.get(query.program_finance_id)

        program_finance_data['yr_1_earnings'] = program_finance.year_1_income
        program_finance_data['yr_2_earnings'] = program_finance.year_2_income
        program_finance_data['yr_3_earnings'] = program_finance.year_3_income
        program_finance_data['cost'] = program_finance.cost
        program_finance_data['tuition_type'] = program_finance.tuition_types.tuition_type
        
        data.append(program_finance_data)

    return data
