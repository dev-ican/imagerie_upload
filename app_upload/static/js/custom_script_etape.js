$('a[id="walk_dir"]').click(function(event) {
	var url_walk = "/admin_page/walk_up/"
	var id_etude = $('a[id="id_etude"]').attr('name');
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}


	if (confirm("Cette entrée sera supprimé définitivement ainsi que tous les enregistrements qui lui sont liés")) {
		$.ajaxSetup({
    		beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	}
    	}
		});

	$.ajax({
		url : url_etude + id_etude + "/",
		data : {
			demande : id_etude
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

$('#msgEtape').change(function(event) {
	x = setTimeout(effaceinfo, 2000);
});

function effaceinfo() {
	$('#msgEtape').text("");
}