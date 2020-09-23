$('select[name="select_etude"]').change(function(event) {
	var url_etude = "/admin_page/upfiles/tris/"
	var id_etude = $(this).children("option:selected").val();
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	console.log(csrftoken)

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
		url : url_etude + id_etude + "/",
		data : {
			demande : id_etude
		},
		type : 'POST',
		success: function(response, status, XHR){
			console.log("SUCCESS");
			$('#ajax').html(response);}
	})
	
});

$("td.clickable").click(function(){
	var url_etude = "/admin_page/upfiles/mod"
	var value = $(this).attr('value');
	var list = $("select[name='select_etude'] option:selected").val();
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
	var td_parent = $( "td.clickable" ).parent('tr').attr('value');

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
			val_jonction : value,
			val_suivi : td_parent,
			val_etude : list,
		},
		type : 'POST',
		success: function(response, status, XHR){
			console.log("SUCCESS");}
	}).done(function(data) {
		var val_data = JSON.parse(data);

		console.log(val_data)
	})

});