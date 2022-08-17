$searchSaveStatus = $('#save_search');

// allow user to sort search results
async function saveSearch(e){
    // e.preventDefault();
    // e.stopPropogation();
    const isChecked = [];

    if ($searchSaveStatus.is(':checked')){
        isChecked.append(true);
    }
    else{
        isChecked.append(false)
    }

    // make AJAX call to API (/saveSearch)

    // get data from input fields
    

    let resp = await axios({
        method: 'post',
        url: 'http://localhost:5000/API/saveSearch',
        data: {
          name: 'test',
          check_status: isChecked
        }
      });

    console.log('Entered Save search')


}


$('#save_search').on("click", saveSearch)