$('#download_export').click(function(event) {
	var url_etude = "/admin_page/centres/download_export/"
	var id_export = $(this).attr('value');
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}


	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    	}
	}
	});

	$.ajax({
		url : url_etude + "/",
		data : {
			demande : id_export
		},
		type : 'POST',
		success: function(response, status, XHR){
			console.log("SUCCESS");
			$('#ajax').html(response);}
	})
	
});

$('#message').change(function(event) {
	x = setTimeout(effaceinfo, 2000);
});

function effaceinfo() {
	$('#message').text("");
}