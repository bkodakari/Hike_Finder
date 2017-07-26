"use strict";

$('#submit').on('click', function (evt) {
    var x = $('#address').val();
    var y = $('#distance').val();
    if (x === "") {
        alert("Address must be filled out");
        return false;
    } else if (y === "") {
        alert("Distance must be filled out");
        return false;
    } else {
      getList(evt);
    }
});


function getList(evt){
  evt.preventDefault();

  $('#json_of_hikes').html('');
  var formInputs = {
    'address':$('#address').val(),
    'distance':$('#distance').val()};
  $.get('/local-hikes.json', formInputs, loadListOfHikes);
}

function loadListOfHikes(data){

  if ($.isEmptyObject(data) === true){
    alert("Search did not return any results, please try again.");
  } else {
    console.log("data:" +data);
    $('#search_results').html('<h3 class="panel-title">Search Results</h3>');
    var arrayTrailNames = [];
    $.each(data, function(key, value){
      arrayTrailNames.push(key);
    });
    console.log("arrayTrailNames"+arrayTrailNames);
    
    
    var arrayTrailLatLng = [];

    for (var i=0; i < arrayTrailNames.length; i++){
      var lat = data[arrayTrailNames[i]][1];
      var lng = data[arrayTrailNames[i]][2];
      var latLng = new google.maps.LatLng(lat, lng);
      arrayTrailLatLng.push(latLng);
      $('#json_of_hikes').append('<a class="list-group-item" href="/trails/'+
        data[arrayTrailNames[i]][4]+'"">'+arrayTrailNames[i]+'</a>');
    }

    var myLatlng = arrayTrailLatLng[0];
    
    var mapOptions = {
      zoom: 11,
      center: myLatlng
    };

    var map = new google.maps.Map(document.getElementById("map"), mapOptions);

    for (var l=0; l < arrayTrailLatLng.length; l++){
      var url = "/trails/"+data[arrayTrailNames[l]][4];
      console.log(data[arrayTrailNames[l]][4]);
      var marker = new google.maps.Marker({
      position: arrayTrailLatLng[l],
      title: arrayTrailNames[l],
      url: url
    });

  // how can i assign a window to each marker? Can't put a function inside a loop.

      // var contentString = '<div id="content">'+
      //       '<div id="siteNotice">'+
      //       '</div>'+
      //       '<h1 id="firstHeading" class="firstHeading">'+arrayTrailNames[l]+'</h1>'+
      //       '<div id="bodyContent">'+
      //       '<p>'+data[arrayTrailNames[l]][3]+'</p>'+
      //       '<p><a href="/trails/'+data[arrayTrailNames[l]][5]+'"">'+arrayTrailNames[l]+'</a></p>'+
      //       '</div>'+
      //       '</div>';
      // var infowindow = new google.maps.InfoWindow({
      //       content: contentString
      //     });
      // marker.addListener('click', function() {
      //   infowindow.open(map, marker);
      // });
    marker.setMap(map);
    google.maps.event.addListener(marker, 'click', function() {
    window.location.href = this.url;
    });
    }
  }
}








