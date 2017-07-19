"use strict";


$(document).ready(function(){
//  Check Radio-box
  $(".rating input:radio").attr("checked", false);
  $('.rating input').click(function () {
    $(".rating span").removeClass('checked');
    $(this).parent().addClass('checked');
  });

  $('input:radio').change( function(){
    var trailId = $('#trailId').data('trailid');
    var rating = this.value;
    var formInputs = {
      'trailId':$('#trailId').data('trailid'),
      'rating':this.value,
      'trailName':$('#trailId').data('trailname')};
    $.get('/ratings.json', formInputs, printRating);
    alert(trailId + rating);
    });
});

function printRating(data){
  alert("Thank You for your rating of: "+data);
}



// $('#rating').on('click', function (e){
//   console.log(e);
//   var name = this.id;
//   console.log('name: ' + name);
//   var stars = $('input[name="star"]:checked').val();
//   console.log("stars: "+stars);
//   alert("name: "+name);
//   console.log("i'm here")
//   //   e.stopPropagation();
//   // e.preventDefault();  

// });


//   var formInputs = {
//     'trailId':$('#trailId').data('trailid'),
//     'stars':$("#"+name:'checked').val()};
//   $.get('/ratings.json', formInputs, printRating);
// });

// function printRating(data){
//   alert("Thank You for your rating of: "+data);
// }


// $('#rating').on('click', function(evt){
//     evt.preventDefault();
//     console.log($('input[name="star"]:checked').val());
//     // Check Radio-box
//     $(".rating input:radio").attr("checked", false);

//     $('.rating input').click(function () {
//         $(".rating span").removeClass('checked');
//         $(this).parent().addClass('checked');
//     });

//     $('input:radio').change(
//       function(){
//         var userRating = this.value;
//         alert(userRating);
//     }); 
// });