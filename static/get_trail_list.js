$('#submit').on('click', getList);

function getList(evt){
  evt.preventDefault();
  document.getElementById('json_of_hikes').innerHTML = ('');
  var formInputs = {
    'address':$('#address').val(),
    'distance':$('#distance').val()};
  $.get('/local-hikes.json', formInputs, checkForData);
  console.log(formInputs);
}

//need intermediate check for data before calling loadListOfHikes... if no data, flash message.


// flawed - logic is reversed and nothing happens when there is no data
function checkForData(data) {
  for(var prop in data) {
    if (prop.hasOwnProperty(prop)){
      alert("Search did not return any results, please try again.");
    } else {
      loadListOfHikes(data);
    }
  }
}

function loadListOfHikes(data){
  var arrayTrailNames = [];
  $.each(data, function(key, value){
    arrayTrailNames.push(key);
  });
  
  var arrayTrailLatLng = [];

  for (var i=0; i < arrayTrailNames.length; i++){
  var lat = data[arrayTrailNames[i]][1];
  var lng = data[arrayTrailNames[i]][2];
  var latLng = new google.maps.LatLng(lat, lng);
  arrayTrailLatLng.push(latLng);
  document.getElementById('json_of_hikes').innerHTML += ('<li>'+'<a href="/trails/'+data[arrayTrailNames[i]][5]+'"">'+arrayTrailNames[i]+'</a></li>');
  }

  var myLatlng = arrayTrailLatLng[0];
  
  var mapOptions = {
    zoom: 11,
    center: myLatlng
  };

  
  var map = new google.maps.Map(document.getElementById("map"), mapOptions);

  for (var l=0; l < arrayTrailLatLng.length; l++){
    var marker = new google.maps.Marker({
    position: arrayTrailLatLng[l],
    title: arrayTrailNames[l],
  });
  marker.setMap(map);
  }
}

function initMap() {

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 9,
    center: {lat: 37.7749, lng: -122.4194}
  });
}






