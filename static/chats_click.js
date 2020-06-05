$(document).ready(function() {
  $('#funcs').hide();
  $('#opt').click(function() {
    $('#opt').hide();
    $('#settings').css({"left":"75px", "bottom":"20px","cursor":"pointer"});
    $('#settings').addClass("hvr-grow")
    $('#funcs').toggle();
  });
  $('#settings').click(function() {
    $('#funcs').hide();
    $('#settings').css({"left":"185px", "bottom":"15px"});
    $('#opt').show();
    $('#settings').removeClass("hvr-grow")
    $('#settings').css({"cursor":"default"});
  });
});
