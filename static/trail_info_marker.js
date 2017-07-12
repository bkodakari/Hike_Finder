"use strict"


function getMappingData(evt){
  evt.preventDefault();

}


$(document).ready(function(evt){
  var x = 
})

    var lat = data[arrayTrailNames[i]][1];
    var lng = data[arrayTrailNames[i]][2];
    var myLatLng = new google.maps.LatLng(lat, lng);
    
    var mapOptions = {
      zoom: 11,
      center: myLatLng
    };

    var map = new google.maps.Map(document.getElementById("map"), mapOptions);

    var marker = new google.maps.Marker({
    position: myLatLng,
    title: ######,
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
    }
