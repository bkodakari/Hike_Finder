function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: {lat: 37.7749, lng: -122.4194}
  });
  var geocoder = new google.maps.Geocoder();
      document.getElementById('submit').addEventListener('submit', function(evt) {
    // evt.preventDefault();
    console.log("in callback");
    geocodeAddress(geocoder, map);
  });
}

window.initMap = initMap;

function geocodeAddress(geocoder, resultsMap) {
  var address = document.getElementById('address').value;
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === 'OK') {
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}
