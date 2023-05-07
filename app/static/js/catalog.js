function ReturnResponse() {
  var max_price = document.getElementById("max_price").value;
  var min_price = document.getElementById("min_price").value;
  var dev = document.getElementById("set_dev").value;
  var id = document.getElementById("set_id").value;
  var title = document.getElementById("set_title").value; 

  response = [max_price, min_price, dev, id, title];

  return response;
}

function SortTable(data, sortby) {

  // Sort the data based on price
  if (sortby) {
    data.sort(function (row1, row2) {
      if (sortby == 'asc') {
        return row1.price - row2.price;
      }
      if (sortby == 'desc') {
        return row2.price - row1.price;
      }
    });
  }
}


function RequestTable(pageNum) {
  return new Promise(function(resolve, reject) {
    $.ajax({
      url: '/games_api/',
      type: 'GET',
      data: {
        page: pageNum
      },
      success: function (response) {
        resolve(response);
      },
      error: function (error) {
        console.log("Error: ", error);
        reject(error);
      }
    });
  });
}


async function SortFunction(sortby, pageNum) {

  const response = await RequestTable(pageNum);
  var data = response.data;
  var filters = ReturnResponse();

  //Debug output. Checks the variables. Not meant for the user to see
  //console.log("PAGE WE'RE ON: ", pageNum);
  //console.log("GIVEN MAX PRICE: ", filters[0]);
  //console.log("GIVEN MIN PRICE: ", filters[1]);
  //console.log("GIVEN DEVELOPER: ", filters[2]);
  //console.log("GIVEN ID: ", filters[3]);


  // Sort the data based on price
  SortTable(data, sortby);


  // Clear the table body
  var table = document.getElementById("tablegames");
  table.classList.add('tableorganizer');
  var tbody = table.getElementsByTagName("tbody")[0];
  tbody.innerHTML = "";

  // Rebuild the table with the sorted rows from scratch.
  for (var i = 0; i < data.length; i++) {

    let condition = true;
    var row = document.createElement("tr");

    //Add the appid value in the table
    var appid = document.createElement("td");
    appid.innerText = data[i].appid;
    appid.classList.add('appid');
    row.appendChild(appid);

    //Add the name value and add the appropriate hyperlink to it
    var name = document.createElement("td");
    const link = document.createElement('a');
    link.href = data[i].appid;
    link.innerText = data[i].name;
    name.appendChild(link);
    name.classList.add('name');
    row.appendChild(name);

    //Formatting price correctly so that it doesn't look awkward in the table
    var price = document.createElement("td");
    if (data[i].price == 0) {
      price.innerText = "Free";
    }
    else {
      price.innerText = "$" + data[i].price;
      var check_number = true;
      for (var char of price.innerText) {
        if (char === '.') {
          check_number = false;
          break;
        }
      }
      if (check_number) {
        price.innerText = "$" + data[i].price + ".00";
      }
      price.classList.add('price');
    }


    row.appendChild(price);

    //Add the developer value
    var developer = document.createElement("td");
    developer.innerText = data[i].developer;
    developer.classList.add('developer');
    row.appendChild(developer);


    //Apply additional filters. The table is rebuilt every time a user presses a filter. The filters remain active on the html page so these will update with the value.
    if (filters[0]) {
      if (data[i].price > Number(filters[0])) {
        condition = false;
      }
    }
    if (filters[1]) { 
      if (data[i].price < Number(filters[1])) {
        condition = false;
      }
    }
    if (filters[2]) {
      if (!data[i].developer.includes(filters[2])) {
        condition = false;
      }
    }
    if (filters[3]) {
      if (!data[i].appid.includes(filters[3])) {
        condition = false;
      }
    }
    if (filters[4]) {
      if (!data[i].name.includes(filters[4])) {
        condition = false;
      }
    }

    if (condition) {
      tbody.appendChild(row);
    }

  }
}


module.exports = {
  ReturnResponse: ReturnResponse,
  SortTable: SortTable,
  SortFunction: SortFunction,
  RequestTable: RequestTable
};

