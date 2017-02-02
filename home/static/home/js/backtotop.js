$(window).scroll(function() {
	if ($(window).scrollTop() > 400) {
		$('a.back-to-top').fadeIn('slow');
	} else {
		$("a.back-to-top").fadeOut("slow");
	}
});


$('a.back-to-top').click(function() {
	$('html, body').animate({
		scrollTop: 0
	}, 700);
	return false;
});