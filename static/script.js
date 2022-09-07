$searchSaveStatus = $('#save_search');
$schoolInput = $('#school1');
$majorDatalist = $('#major1-list');
$majorInput = $('#major1');
$schoolDatalist = $('#school1-list');
$stateInput = $('#school_state');
$stateDatalist = $('#school_state-list');

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
  
  if ($schoolInput.val().length === 0 || $schoolInput.val().length > 10){
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
  $majorDatalist.empty()
  $stateDatalist.empty()

  // $('#selectBox').append($('<option>').val(item).text(optionText))
  for (const item of data.major_list){
    $newOption = $("<option>");
    $newOption.val(item)

    $majorDatalist.append($newOption);
    // $newOption.val() = 
  }

  for (const item of data.state_list){
    $newOption = $("<option>");
    $newOption.val(item)

    $stateDatalist.append($newOption);
  }
  // if (data.type === 'all_majors'){
  //     for (const item of data.major_list){
  //       $newOption = $("<option>");
  //       $newOption.val(item);
    
  //       $majorDatalist.append($newOption);
  //       // $newOption.val() = 
  //     }
  //     console.log('finished all_majors loop')
  // } else if (data.type === 'select'){
  // }

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
  $schoolDatalist.empty();
  $stateDatalist.empty();

  for (const item of data.school_list){
    $newOption = $("<option>");
    $newOption.val(item)

    $schoolDatalist.append($newOption);
  }

  for (const item of data.state_list){
    $newOption = $("<option>");
    $newOption.val(item)

    $stateDatalist.append($newOption);
  }

};

async function processStateInput(e){
  e.preventDefault();

  if ($stateInput.val().length === 0 || $stateInput.val().length === 2){
    let resp = await axios({
      method: 'get',
      url: 'http://localhost:5000/API/processStateInput',
      params: {
        major: `${$majorInput.val()}`,
      }

    });

    const data = resp.data
    updateSchoolOptions(data)
  }
};

function updateSchoolOptions(data){
  $schoolDatalist.empty();
  // update the major list instead
  $stateDatalist.empty();

  for (const item of data.school_list){
    $newOption = $("<option>");
    $newOption.val(item)

    $schoolDatalist.append($newOption);
  }

  for (const item of data.state_list){
    $newOption = $("<option>");
    $newOption.val(item)

    $stateDatalist.append($newOption);
  }

};



$('#save_search').on("click", saveSearch);

$schoolInput.on("keyup", updateMajorList);
$schoolInput.on('click',updateMajorList)

$majorInput.on('keyup', updateSchoolList);

// $stateInput.on('keyup',processStateInput)

// $majorInput.on('click', updateMajorList);

// $schoolInput.on("focusout", updateMajorList);