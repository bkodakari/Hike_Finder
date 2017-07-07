$('#submit').on('click', getList);

function getList(evt){
  evt.preventDefault();
  document.getElementById('json_of_hikes').innerHTML = ('');
  var formInputs = {
    'address':$('#address').val(),
    'distance':$('#distance').val()};
  $.get('/local-hikes.json', formInputs, loadListOfHikes);
  console.log(formInputs);
}

//need intermediate check for data before calling loadListOfHikes... if no data, flash message.

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






