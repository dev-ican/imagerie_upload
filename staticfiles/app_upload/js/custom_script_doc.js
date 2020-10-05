$('#supprDoc').click(function(event) {
	var url_etude = "/doc/deleted/"
	var id_doc = $(this).attr('value');
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}


	if (confirm("Cette entrée sera supprimé définitivement")) {
		$.ajaxSetup({
    		beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	}
    	}
		});

	$.ajax({
		url : url_etude + id_doc + "/",
		data : {
			demande : id_doc
		},
		type : 'POST',
		success: function(response, status, XHR){
			console.log("SUCCESS");
			$('#ajax').html(response);}
	})
	} else {
		  window.alert("La suppréssion est annulée");
		}
	
});

$('#message').change(function(event) {
	x = setTimeout(effaceinfo, 2000);
});

function effaceinfo() {
	$('#message').text("");
}