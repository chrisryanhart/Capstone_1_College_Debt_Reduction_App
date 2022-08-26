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
    
    const $school = $('#school').val()
    const $major = $('#major').val()
    const $degree = $('#degree').val()
    const $household_income = $('#HH-income').val()
    const $home_state = $('#home-state').val()

    // get data from input fields
    // school, major, home_state, credential, HH_income_id
    

    let resp = await axios({
        method: 'post',
        url: 'http://localhost:5000/API/saveSearch',
        data: {
          school: $school,
          major: $major,
          degree: $degree,
          household_income: $household_income,
          home_state: $home_state,
          check_status: isChecked
        }
      });

    console.log('Entered Save search')


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