$(document).ready(function() {
	$(window).scroll(function() {
  	if($(document).scrollTop() > 10) {
    	$('#trans-nav').addClass('shrink');
    	$('#nav').addClass('nnav');
    }
    else {
    $('#trans-nav').removeClass('shrink');
    $('#nav').removeClass('nnav');
    }
  });
});