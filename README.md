# Capstone_College_Value_App

**App Installation Instructions**

1. From the command line interface, pip install requirements.txt into a new venv

2. Create a new Postgres database named 'college_app'

3. Go to API website https://collegescorecard.ed.gov/data/documentation/ and register for an API key

4. Create a secret.py file in the root directory and set variable API_key = YourAPIKey

5. Start the flask application with 'flask run'

API Notes:


URL Link:

**Overview:**

The College Value App helps prospective students find colleges and 4 year degrees with the highest value.  Total college cost and expected major post-graduation income are provided based on the school, major, household income, and the state of residency.  Users can compare different degree and university value combinations by saving the searches to their homepage.  Users can identify and select the higest value based on their career interests.    



**Features Implemented:**

1. User profile creation
	* Enables to save and compare searches
	* Past searches can be reviewed during a future browsing session

2. Find all schools that offer a specific major
 * Once a major is selected the school lists from which to select are updated

3. Find all majors that a single university offers
 * Upon school selection, a list of all majors is displayed in the major search field

4. Search results can be saved by selecting the checkbox

5. Search result comparison is available via the user homepage   


**Step-by-step User guide:**

1. Sign in or create a user profile that specifies household income and the state of residency
	
2. Conduct new search with a university and major of interest

3. Save search if desired

4. Go to the home screen to compare all saved search results

5. Logout once the search session is complete


Technology Stack Used:

* Python Flask used for backend
* Javascript and jQuery used on frontend

Addition Technologies used

1. Flask bcrypt encrypted password protection