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

function printRating(response){
  alert(response);
}


$(document).ready(function(){
//  select button
  $(".favorite input:button").attr("checked", false);
  $('.favorite input:button').click(function () {
    $(".favorite span").removeClass('checked');
    $(this).parent().addClass('checked');
  });

  $('.favorite input:button').click( function(){
    var trailId = $('#trailId').data('trailid');
    var favorite = this.value;
    var formInputs = {
      'trailId':$('#trailId').data('trailid'),
      'favorite':this.value,
      'trailName':$('#trailId').data('trailname')};
    $.post('/add-to-favorites.json', formInputs, printFavorite);
    });
});

function printFavorite(response){
  alert(response.trailName);
}

