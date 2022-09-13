# College Value App

**Overview:**

The College Value App helps prospective students find colleges and 4 year degrees with the highest value.  Total college cost and expected major post-graduation income are provided based on the school, major, household income, and the state of residency.  Users can compare different degree and university value combinations by saving the searches to their homepage.  Users can identify and select the higest value based on their career interests.    

**URL Link:** https://college-value-app.herokuapp.com/

**API Registration:** https://collegescorecard.ed.gov/data/documentation/

**API Documentation:** https://github.com/RTICWDT/open-data-maker/blob/master/API.md


**Features Implemented:**

1. User profile creation
	* Enables to save and compare searches
	* Past searches can be reviewed during a future browsing session

2. Find all schools that offer a specific major
 * Once a major is selected the school lists from which to select are updated
 * This allows the user to identify a list of all schools with their field of study.

3. Find all majors that a single university offers
 * Upon school selection, a list of all majors is displayed in the major search field
 * If a user has a potential school identified, they can quickly see all the major options available

4. Search results can be saved by selecting the checkbox
 * Users can save search results to compare later

5. Search result comparison is available via the user homepage   
 * Users can compare all school values on a single page


**Step-by-step User guide:**

1. Sign in or create a user profile that specifies household income and the state of residency
	
2. Conduct new search with a university and major of interest

3. Save search if desired

4. Go to the home screen to compare all saved search results

5. Logout once the search session is complete


**Technology Stack Used:**

* Python Flask used for backend
* Javascript and jQuery used on frontend

Addition Technologies used

1. Flask bcrypt encrypted password protection



**App Installation Instructions if running locally**

1. Clone the respository to a new directory on your local machine

2. From the command line interface, pip install requirements.txt into a new venv

2. Create a new Postgres database named 'college_app'

3. Go to API website https://collegescorecard.ed.gov/data/documentation/ and register for an API key

4. Create a .env file in the root directory and set variable API_key = YourAPIKey

5. Start the flask application with 'flask run'


**Notes on API Data**

* Cost and earnings data is limited to students that received federal loans
* In-state and public colleges are able to provide an adjusted net cost
* Out-of-state public colleges do not have data available; Accordingly, the out-of-state cost was calculated as the full tuition, with no reduction based on household income, plus all fees including room & board and books.


