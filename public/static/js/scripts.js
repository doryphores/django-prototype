jQuery(function($) {
	$("div.data-inspector h3").not(".error").click(function () {
		$(this).next().slideToggle(200);
	});
	
	$("#project-settings").not(".open").each(function () {
		var panel = $(this);
		var toggle = $('<a href="#" id="settings-toggle">Configure</a>').insertBefore(this);
		toggle.click(function (e) {
			e.preventDefault();
			panel.slideToggle(200);
		});
	});
	
	$(".async").submit(function (e) {
		e.preventDefault();
		form = $(this).addClass("working");
		$.post(form.attr('action'), form.serialize(), function (data) {
			form.removeClass("working");
			self.location = data;
		});
	});
});