$searchSaveStatus = $('#save_search');
$schoolInput = $('#school1');
$majorDatalist = $('#major1-list');
$majorInput = $('#major1');
$schoolDatalist = $('#school1-list');

// allow user to sort search results
async function saveSearch(e){
    // e.preventDefault();
    // e.stopPropogation();
    let isChecked = null;

    if ($searchSaveStatus.is(':checked')){
      isChecked = true
    }
    else{
      isChecked = false
    }
    
    // get variables from DB schema
    const $school = $('#school').val()
    const $major = $('#major').val()
    const $degree = $('#degree').val();
    const $householdIncome = $('#HH-income').val();
    const $homeState = $('#home-state').val();
    const $schoolState = $('#school-state').val();

    const $cost = $('#cost').val();
    const $incomeYr1 = $('#income-year1').val();
    const $incomeYr2 = $('#income-year2').val();
    const $incomeYr3 = $('#income-year3').val();
    const $tuitionType = $('#tuition-type').val();

    // const $savedQueryId = $('#savedQuery').val();
    const $programFinanceId = $('#program-finance').val();

    // if hidden inputs exist, select elements


    // get data from input fields
    // school, major, home_state, credential, HH_income_id
    
    // add query id to the table
    // query id can only be assigned after the search is saved
    let resp = await axios({
        method: 'post',
        url: 'http://localhost:5000/API/saveSearch',
        data: {
          school: $school,
          major: $major,
          degree: $degree,
          household_income: $householdIncome,
          home_state: $homeState,
          school_state: $schoolState,
          cost: $cost,
          income_yr1: $incomeYr1,
          income_yr2: $incomeYr2,
          income_yr3: $incomeYr3,
          tuition_type: $tuitionType,
          program_finance_id: $programFinanceId,
          // saved_query_id: $savedQueryId,
          check_status: isChecked
        }
      });

    // append saved_query id to the html table in the DOM


    const data = resp.data;

    if (data.status === 'Program finance added to database'){
      $tr = $searchSaveStatus.closest('tr');

      // $savedQueryInput = `<input id="savedQuery" type="hidden" value="${data.saved_query_id}">`;
      $programFinanceInput = `<input id="program-finance" type="hidden" value="${data.program_finance_id}">`;
      
      // $tr.append($savedQueryInput);
      $tr.append($programFinanceInput);
    } 
    else if (data.status === 'Program finance deleted from database'){
      // select input id
      // remove from input from DOM
      $('#program-finance').remove();

      console.log('in else statement');

    }

    
    console.log('Entered Save search');


}

async function updateMajorList(e){
  e.preventDefault();
  console.log('entered update major list')
  
  if ($schoolInput.val().length === 0 || $schoolInput.val().length > 4){
    let resp = await axios({
      method: 'get',
      url: 'http://localhost:5000/API/findMajors',
      params: {
        school: `${$schoolInput.val()}`,
        // major: $major,
        // degree: $degree,
        // household_income: $household_income,
        // home_state: $home_state,
        // check_status: isChecked
      }
    });

    const data = resp.data;

    updateMajorOptions(data);
  }
  else{
    
  }
};

function updateMajorOptions(data){
  $schoolDatalist.empty()

  // $('#selectBox').append($('<option>').val(item).text(optionText))

  for (const item of data.major_list){
    $newOption = $("<option>");
    $newOption.val(item)

    $schoolDatalist.append($newOption);
    // $newOption.val() = 
  }
  
  const test =1;

  // <option value="Cell/Cellular Biology and Anatomical Sciences.">
                
  //                   </option>

};

async function updateSchoolList(e){
  e.preventDefault();

  if ($majorInput.val().length === 0 || $majorInput.val().length > 4){
    let resp = await axios({
      method: 'get',
      url: 'http://localhost:5000/API/findSchools',
      params: {
        major: `${$majorInput.val()}`,
      }

    });

    const data = resp.data
    updateSchoolOptions(data)
  }
};

function updateSchoolOptions(data){
  $schoolDatalist.empty()

  for (const item of data.school_list){
    $newOption = $("<option>");
    $newOption.val(item)

    $schoolDatalist.append($newOption);
  }
};

$('#save_search').on("click", saveSearch);

$schoolInput.on("keyup", updateMajorList);
$majorInput.on('keyup', updateSchoolList);