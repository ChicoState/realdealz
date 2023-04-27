async function SortFunction(sortby, pageNum) {

    //Calls the games_api view and grabs the page number we're on. The page it sends back is what we are filtering.
    $.ajax({
      url: '/games_api/',
      type: 'GET',
      data: {
        page: pageNum
      },
      success: function(response) {
        var data = response.data;
        var max_price = document.getElementById("max_price").value;
        var min_price = document.getElementById("min_price").value;
        var dev = document.getElementById("set_dev").value;
        var id = document.getElementById("set_id").value;
        var title = document.getElementById("set_title").value;
      
        //Debug output. Checks the variables. Not meant for the user to see
        //console.log("PAGE WE'RE ON: ", pageNum);
        //console.log("GIVEN MAX PRICE: ", max_price);
        //console.log("GIVEN MIN PRICE: ", min_price);
        //console.log("GIVEN DEVELOPER: ", dev);
        //console.log("GIVEN ID: ", id);
    
    
        // Sort the data based on price
        if (sortby)
        {
          data.sort(function(row1, row2) {
            if (sortby == 'asc') {
              return row1.price - row2.price;
            }
            if (sortby == 'desc') {
              return row2.price - row1.price;
            }
    
          });      
        }
    
    
    
        // Clear the table body
        var table = document.getElementById("tablegames");
        table.classList.add('tableorganizer');
        var tbody = table.getElementsByTagName("tbody")[0];
        tbody.innerHTML = "";
    
        // Rebuild the table with the sorted rows from scratch.
        for (var i = 0; i < data.length; i++) {
    
          let condition = true;
          var row = document.createElement("tr");
    
          var appid = document.createElement("td");
          appid.innerText = data[i].appid;
          appid.classList.add('appid');
          row.appendChild(appid);
    
          var name = document.createElement("td");
          const link = document.createElement('a');
          link.href = data[i].appid;
          link.innerText = data[i].name;
          name.appendChild(link);
          name.classList.add('name');
          row.appendChild(name);
    
          //Formatting price correctly so that it doesn't look awkward in the table
          var price = document.createElement("td");
          if (data[i].price == 0)
          {
            price.innerText = "Free";
          }
          else
          {
            price.textContent = "$" + data[i].price;
            var check_number = true;
            var priceLength = price.textContent.length;
            for (var char of price.textContent)
            {
              if (char === '.')
              {
                check_number = false;
                break;
              }
            }    
            if (check_number)
            {
              price.textContent = "$" + data[i].price + ".00";
            }
            price.classList.add('price');
          }
    
    
          row.appendChild(price);
    
          var developer = document.createElement("td");
          developer.innerText = data[i].developer;
          developer.classList.add('developer');
          row.appendChild(developer);
    
    
          //Apply additional filters. The table is rebuilt every time a user presses a filter. The filters remain active on the html page so these will update with the value.
          if (max_price)
          {
            if (data[i].price >= max_price)
            {
              condition = false;
            }
          }
          if (min_price)
          {
            if (data[i].price < min_price)
            {
              condition = false;
            }
          }
          if (dev)
          {
            if (!data[i].developer.includes(dev))
            {
              condition = false;
            }
          }
          if (id)
          {
            if (data[appid] != appid)
            {
              condition = false;
            }       
          }
          if (title)
          {
            if (!data[i].name.includes(title))
            {
              condition = false;
            }    
          }
    
          if (condition)
          {
            tbody.appendChild(row);
          }
    
        }

      },
      error: function(error) {
        console.log(error);
      }
    });
  }

  //This function runs SortFunction upon loading the page. Only way to turn 0 -> Free in price
  window.onload = function() {
    var params = new URLSearchParams(window.location.search);
    var page = params.get('page');
    SortFunction(undefined, page);
  };
