"use strict"

$(document).ready(getMappingData);

function getMappingData(){
  var trailId = $('#trailId').data('trailid');

  var formInput = {
    'trail_id':trailId,
  };

  $.get('/trail/'+trailId+'.json', formInput, setMarker);
}

function setMarker(data){
  var lat = data['latitude'];
  var lng = data['longitude'];
  var myLatLng = new google.maps.LatLng(lat, lng);

  var mapOptions = {
  zoom: 14,
  center: myLatLng
  };

  var map = new google.maps.Map(document.getElementById('map'), mapOptions);

  var marker = new google.maps.Marker({
  position: myLatLng,
  title: data['name']
  });

  marker.setMap(map);

  var contentString = '<div id="content">'+
                      '<div id="siteNotice">'+'</div>'+
                      '<h4 id="firstHeading" class="firstHeading">'+data['name']+'</h3>'+
                      '<div id="bodyContent">'+
                      '<p>'+data['description']+'</p>'+
                      '</div>'+'</div>';
  
  var infowindow = new google.maps.InfoWindow({
    content: contentString
  });
  
  marker.addListener('click', function() {
        infowindow.open(map, marker);
  });
}



  // how can i assign a window to each marker? Can't put a function inside a loop.


