"use strict";


$(document).ready(function(){
//  Check Radio-box
  $(".rating input:radio").attr("checked", false);
  $('.rating input').click(function () {
    $(".rating span").removeClass('checked');
    $(this).parent().addClass('checked');
  });

  $('.rating input:radio').change( function(){
    var trailId = $('#trailId').data('trailid');
    var rating = this.value;
    var formInputs = {
      'trailId':$('#trailId').data('trailid'),
      'rating':this.value,
      'trailName':$('#trailId').data('trailname')};
    $.post('/ratings.json', formInputs, printRating);
    });
});

function printRating(data){
  alert("Thank You for your rating of: "+data+"stars");
}


$(function () { // this is the jquery shortcut for document.ready()

  function addToFavorites(evt) {

    var id = this.id; // this is the id on the button we clicked, which is the image's id

      $.post("/add-to-favorites.json", {'id': id, 'trailId':$('#trailId').data('trailid'),
             'trailName':$('#trailId').data('trailname')}, addToFavoritesSuccess);
    }

    function addToFavoritesSuccess(result) {
        alert("Thank You, "+result.trailName+" has been added to your list of favorites."); 

        var id = result.id;

        $('#' + id).css('color', 'red'); // give our user some feedback
    }

    $('#heart').click(addToFavorites);

}); 








// $(document).ready(function(){
// //  Check Radio-box
//   $(".favorite input:radio").attr("checked", false);
//   $('.favorite input').click(function () {
//     $(".favorite span").removeClass('checked');
//     $(this).parent().addClass('checked');
//   });

//   $('input:radio').change( function(){
//     var trailId = $('#trailId').data('trailid');
//     var favorite = this.value;
//     var formInputs = {
//       'trailId':$('#trailId').data('trailid'),
//       'favorite':this.value,
//       'trailName':$('#trailId').data('trailname')};
//     $.get('/favorite.json', formInputs, printFavorite);
//     alert(trailId + favorite);
//     });
// });

// function printFavorite(data){
//   alert("Thank You, "+data+" has been added to your list of favorites.");
// }