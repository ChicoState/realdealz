//This function runs SortFunction upon loading the page. Only way to turn 0 -> Free in price
window.onload = function () {
  var params = new URLSearchParams(window.location.search);
  var page = params.get('page');
  SortFunction(undefined, page);
};