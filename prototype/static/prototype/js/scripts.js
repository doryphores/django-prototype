jQuery(function($) {
	$("div.data-inspector h3").not(".error").click(function () {
		$(this).next().slideToggle(200);
	});
});