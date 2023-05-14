//Run these commands to run these tests correctly
//npm init (Need a package.json in directory)
//npm install jest --save-dev



//npm install jsdom
const { JSDOM } = require('jsdom');
const Catalog = require('./catalog');

//npm install jquery
const $ = require('jquery');




//THIS FUNCTION IS A MODIFIED SORTFUNCTION() FOUND IN catalog.js to allow easier testing due tot the await portion used in SortFunction
async function SortFunctionTest(sortby, response) {

  data = response.data;
  var filters = Catalog.ReturnResponse();
  Catalog.BuildTable(sortby, filters, data);
}



/*////////////////
AJAX TESTING (IMPORTANT FOR TESTING)
*/////////////////

//RequestTable in catalog.js makes a AJAX request that communicates with the database and returns it after finding what page Django's paginator is on
//Test_Response() is equal to RequestTable() however having the AJAX response here doesn't create an error for some reason compared to calling Catalog.RequestTable()
//THERE IS NOT DIFFERENCE BETWEEEN THIS FUNCTION AND REQUESTTABLE()
function Test_Response(pageNum) {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: '/games_api/',
      type: 'GET',
      data: { page: pageNum },
      success: function (response) {
        resolve(response);      
      },
      error: function (xhr, status, error) {
        reject(error);
      }
    });
  });
};

//The fake response the testing suite will use from ajax
jest.mock('jquery', () => ({
  ajax: jest.fn().mockImplementation((params) => {
    params.success({
      data: [
        { appid: "1", name: 'Game 1', price: '100', developer: 'A Games' },
        { appid: "2", name: 'Game 2', price: '200', developer: 'B Games' },
        { appid: "3", name: 'Game 3', price: '150.00', developer: 'C Games' },
        { appid: "4", name: 'Game 4', price: '0.0', developer: 'D Games' },
      ]
    });
  })
}));


/*////////////////
UNIT TESTS
*/////////////////

test('Smoke Test', () => {
  expect(1).toBe(1);
});

describe('ReturnResponse() handles undefined HTML values', () => {
  it('If no value is given, all entries will be empty (undefined)', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price">
          <input type="text" id="min_price">
          <input type="text" id="set_dev">
          <input type="text" id="set_id">
          <input type="text" id="set_title">
        </body>
      </html>
    `);

    global.document = dom.window.document;

    const result = Catalog.ReturnResponse();
    expect(result[0]).toBe("");
    expect(result[1]).toBe("");
    expect(result[2]).toBe("");
    expect(result[3]).toBe("");
    expect(result[4]).toBe("");
  });
});


describe('ReturnResponse() detects given HTML values', () => {
  it('If a user enters a value, the function will return the same value', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price" value="100">
          <input type="text" id="min_price">
          <input type="text" id="set_dev">
          <input type="text" id="set_id">
          <input type="text" id="set_title">
        </body>
      </html>
    `);

    global.document = dom.window.document;


    const result = Catalog.ReturnResponse();
    expect(result[0]).toBe("100");
    expect(result[1]).toBe("");
    expect(result[2]).toBe("");
    expect(result[3]).toBe("");
    expect(result[4]).toBe("");
  });
});


test('Test_Response() returns an object', () => {
  return Test_Response(1).then(response => {
    expect(response).toBeDefined();
    expect(typeof response).toBe('object');
  });
});



test('Test_Response() returns the correct length of data', () => {
  return Test_Response(1).then(response => {

    data = response.data;
    expect(data.length).toBe(4);
  });
});

test('Test_Response() returns the correct data', () => {
  return Test_Response(1).then(response => {

    data = response.data;
    expect(data[0].appid).toBe("1");
    expect(data[0].name).toBe("Game 1");
    expect(data[0].price).toBe("100");
    expect(data[0].developer).toBe("A Games");
    expect(data[1].appid).toBe("2");
    expect(data[1].name).toBe("Game 2");
    expect(data[1].price).toBe("200");
    expect(data[1].developer).toBe("B Games");
    expect(data[2].appid).toBe("3");
    expect(data[2].name).toBe("Game 3");
    expect(data[2].price).toBe("150.00");
    expect(data[2].developer).toBe("C Games");
    expect(data[3].appid).toBe("4");
    expect(data[3].name).toBe("Game 4");
    expect(data[3].price).toBe("0.0");
    expect(data[3].developer).toBe("D Games");
  
  });
});


test('Sort Ascending Order Price SortTable()', () => {
  return Test_Response(1).then(response => {

    data = response.data;
    Catalog.SortTable(data, 'desc');
    expect(data[0].price).toBe("200");
    expect(data[1].price).toBe("150.00");
    expect(data[2].price).toBe("100");
    expect(data[3].price).toBe("0.0");
  });
});

test('Sort Descending Order Price SortTable()', () => {
  return Test_Response(1).then(response => {

    data = response.data;
    Catalog.SortTable(data, 'asc');
    expect(data[0].price).toBe("0.0");
    expect(data[1].price).toBe("100");
    expect(data[2].price).toBe("150.00");
    expect(data[3].price).toBe("200");
  });
});



describe('Validates SortFunction()', () => {
  it('SortFunction will return the correct data upon use', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price">
          <input type="text" id="min_price">
          <input type="text" id="set_dev">
          <input type="text" id="set_id">
          <input type="text" id="set_title">
          <table id="tablegames">
            <thead>
              <tr>
                <th>ID</th>
                <th>Game Title</th>
                <th>Price</th>
                <th>Developer</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="id">PLACEHOLDER</td>
                <td class="name">PLACEHOLDER</td>
                <td class="price">PLACEHOLDER</td>
                <td class="developer">PLACEHOLDER</td>
              </tr>
            </tbody>
          </table>
        </body>
      </html>
    `);

    //Emulates the html
    global.document = dom.window.document;
    Test_Response(1).then(response => {

      //Grab the table from the html file
      const tablegames = document.getElementById('tablegames');

      //Reminder: This overwrites the old table and completely replaces it. PLACEHOLDER should be gone.
      SortFunctionTest(' ', response);

      

      //Tests the content of the table and make sure they are correct
      const rows = tablegames.getElementsByTagName('tr');
      var cells = rows[1].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("1");
      expect(cells[1].innerText).toBe("Game 1");
      expect(cells[2].innerText).toBe("$100.00");
      expect(cells[3].innerText).toBe("A Games");


      cells = rows[2].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("2");
      expect(cells[1].innerText).toBe("Game 2");
      expect(cells[2].innerText).toBe("$200.00");
      expect(cells[3].innerText).toBe("B Games");


      cells = rows[3].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("3");
      expect(cells[1].innerText).toBe("Game 3");
      expect(cells[2].innerText).toBe("$150.00");
      expect(cells[3].innerText).toBe("C Games");

      cells = rows[4].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("4");
      expect(cells[1].innerText).toBe("Game 4");
      expect(cells[2].innerText).toBe("Free");
      expect(cells[3].innerText).toBe("D Games");
    });
  });
});


describe('Ascending Order SortFunction()', () => {
  it('Sorts the table entries in ascending order with price', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price">
          <input type="text" id="min_price">
          <input type="text" id="set_dev">
          <input type="text" id="set_id">
          <input type="text" id="set_title">
          <table id="tablegames">
            <thead>
              <tr>
                <th>ID</th>
                <th>Game Title</th>
                <th>Price</th>
                <th>Developer</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="id">PLACEHOLDER</td>
                <td class="name">PLACEHOLDER</td>
                <td class="price">PLACEHOLDER</td>
                <td class="developer">PLACEHOLDER</td>
              </tr>
            </tbody>
          </table>
        </body>
      </html>
    `);

    //Emulates the html
    global.document = dom.window.document;
    Test_Response(1).then(response => {

      //Grab the table from the html file
      const tablegames = document.getElementById('tablegames');

      //Reminder: This overwrites the old table and completely replaces it. PLACEHOLDER should be gone.
      SortFunctionTest('asc', response);

      //Tests the content of the table and make sure they are correct
      const rows = tablegames.getElementsByTagName('tr');

      var cells = rows[1].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("4");
      expect(cells[1].innerText).toBe("Game 4");
      expect(cells[2].innerText).toBe("Free");
      expect(cells[3].innerText).toBe("D Games");

      cells = rows[2].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("1");
      expect(cells[1].innerText).toBe("Game 1");
      expect(cells[2].innerText).toBe("$100.00");
      expect(cells[3].innerText).toBe("A Games");

      cells = rows[3].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("3");
      expect(cells[1].innerText).toBe("Game 3");
      expect(cells[2].innerText).toBe("$150.00");
      expect(cells[3].innerText).toBe("C Games");

      cells = rows[4].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("2");
      expect(cells[1].innerText).toBe("Game 2");
      expect(cells[2].innerText).toBe("$200.00");
      expect(cells[3].innerText).toBe("B Games");
    });
  });
});


describe('Descending Order SortFunction()', () => {
  it('Sorts the table entries in descending order with price', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price">
          <input type="text" id="min_price">
          <input type="text" id="set_dev">
          <input type="text" id="set_id">
          <input type="text" id="set_title">
          <table id="tablegames">
            <thead>
              <tr>
                <th>ID</th>
                <th>Game Title</th>
                <th>Price</th>
                <th>Developer</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="id">PLACEHOLDER</td>
                <td class="name">PLACEHOLDER</td>
                <td class="price">PLACEHOLDER</td>
                <td class="developer">PLACEHOLDER</td>
              </tr>
            </tbody>
          </table>
        </body>
      </html>
    `);

    //Emulates the html
    global.document = dom.window.document;
    Test_Response(1).then(response => {

      //Grab the table from the html file
      const tablegames = document.getElementById('tablegames');

      //Reminder: This overwrites the old table and completely replaces it. PLACEHOLDER should be gone.
      SortFunctionTest('desc', response);

      //Tests the content of the table and make sure they are correct
      const rows = tablegames.getElementsByTagName('tr');

      var cells = rows[1].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("2");
      expect(cells[1].innerText).toBe("Game 2");
      expect(cells[2].innerText).toBe("$200.00");
      expect(cells[3].innerText).toBe("B Games");

      cells = rows[2].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("3");
      expect(cells[1].innerText).toBe("Game 3");
      expect(cells[2].innerText).toBe("$150.00");
      expect(cells[3].innerText).toBe("C Games");

      cells = rows[3].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("1");
      expect(cells[1].innerText).toBe("Game 1");
      expect(cells[2].innerText).toBe("$100.00");
      expect(cells[3].innerText).toBe("A Games");

      cells = rows[4].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("4");
      expect(cells[1].innerText).toBe("Game 4");
      expect(cells[2].innerText).toBe("Free");
      expect(cells[3].innerText).toBe("D Games");

    });
  });
});

describe('No result SortFunction()', () => {
  it('Ensures that the search returns nothing if given no match', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price">
          <input type="text" id="min_price" value="999">
          <input type="text" id="set_dev">
          <input type="text" id="set_id">
          <input type="text" id="set_title">
          <table id="tablegames">
            <thead>
              <tr>
                <th>ID</th>
                <th>Game Title</th>
                <th>Price</th>
                <th>Developer</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="id">PLACEHOLDER</td>
                <td class="name">PLACEHOLDER</td>
                <td class="price">PLACEHOLDER</td>
                <td class="developer">PLACEHOLDER</td>
              </tr>
            </tbody>
          </table>
        </body>
      </html>
    `);

    //Emulates the html
    global.document = dom.window.document;
    Test_Response(1).then(response => {

      //Grab the table from the html file
      const tablegames = document.getElementById('tablegames');

      //Reminder: This overwrites the old table and completely replaces it. PLACEHOLDER should be gone.
      SortFunctionTest('', response);

      //Tests the content of the table and make sure they are correct
      const rows = tablegames.getElementsByTagName('tr');
      expect(rows.length).toBe(1);
    });
  });
});


describe('Specified ID SortFunction()', () => {
  it('Look for the ID of a game that the user specified through the view', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price">
          <input type="text" id="min_price">
          <input type="text" id="set_dev">
          <input type="text" id="set_id" value="1">
          <input type="text" id="set_title">
          <table id="tablegames">
            <thead>
              <tr>
                <th>ID</th>
                <th>Game Title</th>
                <th>Price</th>
                <th>Developer</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="id">PLACEHOLDER</td>
                <td class="name">PLACEHOLDER</td>
                <td class="price">PLACEHOLDER</td>
                <td class="developer">PLACEHOLDER</td>
              </tr>
            </tbody>
          </table>
        </body>
      </html>
    `);

    //Emulates the html
    global.document = dom.window.document;
    Test_Response(1).then(response => {

      //Grab the table from the html file
      const tablegames = document.getElementById('tablegames');

      //Reminder: This overwrites the old table and completely replaces it. PLACEHOLDER should be gone.
      SortFunctionTest('', response);

      //Tests the content of the table and make sure they are correct
      const rows = tablegames.getElementsByTagName('tr');
      expect(rows.length).toBe(2);

      var cells = rows[1].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("1");
      expect(cells[1].innerText).toBe("Game 1");
      expect(cells[2].innerText).toBe("$100.00");
      expect(cells[3].innerText).toBe("A Games");
    });
  });
});


describe('Specified Name SortFunction()', () => {
  it('Look for the name of a game that the user specified through the view', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price">
          <input type="text" id="min_price">
          <input type="text" id="set_dev">
          <input type="text" id="set_id"">
          <input type="text" id="set_title" value="Game 3">
          <table id="tablegames">
            <thead>
              <tr>
                <th>ID</th>
                <th>Game Title</th>
                <th>Price</th>
                <th>Developer</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="id">PLACEHOLDER</td>
                <td class="name">PLACEHOLDER</td>
                <td class="price">PLACEHOLDER</td>
                <td class="developer">PLACEHOLDER</td>
              </tr>
            </tbody>
          </table>
        </body>
      </html>
    `);

    //Emulates the html
    global.document = dom.window.document;
    Test_Response(1).then(response => {

      //Grab the table from the html file
      const tablegames = document.getElementById('tablegames');

      //Reminder: This overwrites the old table and completely replaces it. PLACEHOLDER should be gone.
      SortFunctionTest('', response);

      //Tests the content of the table and make sure they are correct
      const rows = tablegames.getElementsByTagName('tr');
      expect(rows.length).toBe(2);

      var cells = rows[1].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("3");
      expect(cells[1].innerText).toBe("Game 3");
      expect(cells[2].innerText).toBe("$150.00");
      expect(cells[3].innerText).toBe("C Games");
    });
  });
});

describe('Specified Developer SortFunction()', () => {
  it('This test looks for any developer that has a C in its name. It also checks if SortFunction() works on partial matches', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price">
          <input type="text" id="min_price">
          <input type="text" id="set_dev" value="C">
          <input type="text" id="set_id">
          <input type="text" id="set_title">
          <table id="tablegames">
            <thead>
              <tr>
                <th>ID</th>
                <th>Game Title</th>
                <th>Price</th>
                <th>Developer</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="id">PLACEHOLDER</td>
                <td class="name">PLACEHOLDER</td>
                <td class="price">PLACEHOLDER</td>
                <td class="developer">PLACEHOLDER</td>
              </tr>
            </tbody>
          </table>
        </body>
      </html>
    `);

    //Emulates the html
    global.document = dom.window.document;
    Test_Response(1).then(response => {

      //Grab the table from the html file
      const tablegames = document.getElementById('tablegames');

      //Reminder: This overwrites the old table and completely replaces it. PLACEHOLDER should be gone.
      SortFunctionTest('', response);

      //Tests the content of the table and make sure they are correct
      const rows = tablegames.getElementsByTagName('tr');
      expect(rows.length).toBe(2);

      var cells = rows[1].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("3");
      expect(cells[1].innerText).toBe("Game 3");
      expect(cells[2].innerText).toBe("$150.00");
      expect(cells[3].innerText).toBe("C Games");
    });
  });
});


describe('Multiple Parameters SortFunction()', () => {
  it('This test use all HTML inputs and checks if SortFunction() can handle them', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price" value="1000">
          <input type="text" id="min_price" value="100">
          <input type="text" id="set_dev" value="C">
          <input type="text" id="set_id" value="3">
          <input type="text" id="set_title" value="Game 3">
          <table id="tablegames">
            <thead>
              <tr>
                <th>ID</th>
                <th>Game Title</th>
                <th>Price</th>
                <th>Developer</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="id">PLACEHOLDER</td>
                <td class="name">PLACEHOLDER</td>
                <td class="price">PLACEHOLDER</td>
                <td class="developer">PLACEHOLDER</td>
              </tr>
            </tbody>
          </table>
        </body>
      </html>
    `);

    //Emulates the html
    global.document = dom.window.document;
    Test_Response(1).then(response => {

      //Grab the table from the html file
      const tablegames = document.getElementById('tablegames');

      //Reminder: This overwrites the old table and completely replaces it. PLACEHOLDER should be gone.
      SortFunctionTest('', response);

      //Tests the content of the table and make sure they are correct
      const rows = tablegames.getElementsByTagName('tr');
      expect(rows.length).toBe(2);

      var cells = rows[1].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("3");
      expect(cells[1].innerText).toBe("Game 3");
      expect(cells[2].innerText).toBe("$150.00");
      expect(cells[3].innerText).toBe("C Games");
    });
  });
});


describe('Changing Values During Execution SortFunction()', () => {
  it('User can add more filters at any time. SortFunction() should handle them gracefully', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price">
          <input type="text" id="min_price">
          <input type="text" id="set_dev">
          <input type="text" id="set_id">
          <input type="text" id="set_title">
          <table id="tablegames">
            <thead>
              <tr>
                <th>ID</th>
                <th>Game Title</th>
                <th>Price</th>
                <th>Developer</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="id">PLACEHOLDER</td>
                <td class="name">PLACEHOLDER</td>
                <td class="price">PLACEHOLDER</td>
                <td class="developer">PLACEHOLDER</td>
              </tr>
            </tbody>
          </table>
        </body>
      </html>
    `);

    //Emulates the html
    global.document = dom.window.document;
    Test_Response(1).then(response => {

      //Grab the table from the html file
      const tablegames = document.getElementById('tablegames');

      //Reminder: This overwrites the old table and completely replaces it. PLACEHOLDER should be gone.
      SortFunctionTest('', response);

      //Tests the content of the table and make sure they are correct
      rows = tablegames.getElementsByTagName('tr');
      expect(rows.length).toBe(5);


      const price1 = dom.window.document.getElementById('min_price');
      price1.setAttribute('value', '100');
      const price2 = dom.window.document.getElementById('max_price');
      price2.setAttribute('value', '150');      
      SortFunctionTest('', response);
      rows = tablegames.getElementsByTagName('tr');
      expect(rows.length).toBe(3);

      const id = dom.window.document.getElementById('set_id');
      id.setAttribute('value', '3');
      SortFunctionTest('', response);     
      rows = tablegames.getElementsByTagName('tr');
      var cells = rows[1].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("3");
      expect(cells[1].innerText).toBe("Game 3");
      expect(cells[2].innerText).toBe("$150.00");
      expect(cells[3].innerText).toBe("C Games");
    });
  });
});


describe('Final Test SortFunction()', () => {
  it('Applying and Removing Filters, putting the list in order all in one instance', () => {
    const dom = new JSDOM(`
      <html>
        <body>
          <input type="text" id="max_price">
          <input type="text" id="min_price">
          <input type="text" id="set_dev">
          <input type="text" id="set_id">
          <input type="text" id="set_title">
          <table id="tablegames">
            <thead>
              <tr>
                <th>ID</th>
                <th>Game Title</th>
                <th>Price</th>
                <th>Developer</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="id">PLACEHOLDER</td>
                <td class="name">PLACEHOLDER</td>
                <td class="price">PLACEHOLDER</td>
                <td class="developer">PLACEHOLDER</td>
              </tr>
            </tbody>
          </table>
        </body>
      </html>
    `);

    //Emulates the html
    global.document = dom.window.document;
    Test_Response(1).then(response => {

      //Grab the table from the html file
      const tablegames = document.getElementById('tablegames');
      SortFunctionTest('', response);
      rows = tablegames.getElementsByTagName('tr');
      expect(rows.length).toBe(5);
    
      SortFunctionTest('asc', response);
      rows = tablegames.getElementsByTagName('tr');
      expect(rows.length).toBe(5);

      const price1 = dom.window.document.getElementById('min_price');
      price1.setAttribute('value', '100');
      const price2 = dom.window.document.getElementById('max_price');
      price2.setAttribute('value', '150');  
      SortFunctionTest('desc', response);
      rows = tablegames.getElementsByTagName('tr');
      expect(rows.length).toBe(3);


      var cells = rows[1].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("3");
      expect(cells[1].innerText).toBe("Game 3");
      expect(cells[2].innerText).toBe("$150.00");
      expect(cells[3].innerText).toBe("C Games");

      cells = rows[2].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("1");
      expect(cells[1].innerText).toBe("Game 1");
      expect(cells[2].innerText).toBe("$100.00");
      expect(cells[3].innerText).toBe("A Games");


      price1.setAttribute('value', '');
      price2.setAttribute('value', '');
      SortFunctionTest('asc', response);
      rows = tablegames.getElementsByTagName('tr');
      expect(rows.length).toBe(5);

      rows = tablegames.getElementsByTagName('tr');

      var cells = rows[1].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("4");
      expect(cells[1].innerText).toBe("Game 4");
      expect(cells[2].innerText).toBe("Free");
      expect(cells[3].innerText).toBe("D Games");

      cells = rows[2].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("1");
      expect(cells[1].innerText).toBe("Game 1");
      expect(cells[2].innerText).toBe("$100.00");
      expect(cells[3].innerText).toBe("A Games");

      cells = rows[3].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("3");
      expect(cells[1].innerText).toBe("Game 3");
      expect(cells[2].innerText).toBe("$150.00");
      expect(cells[3].innerText).toBe("C Games");

      cells = rows[4].getElementsByTagName('td');
      expect(cells[0].innerText).toBe("2");
      expect(cells[1].innerText).toBe("Game 2");
      expect(cells[2].innerText).toBe("$200.00");
      expect(cells[3].innerText).toBe("B Games");
    });
  });
});
