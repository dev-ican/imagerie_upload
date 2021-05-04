$('button[name="del_etudeetape"]').on("click", function(){
	var url_etude = "/admin_page/etapes/deletelink";

	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
	var id_parent = $('button[name="clikable"]').parent('td').attr('value');
	var type_parent = $('button[name="clikable"]').parent('td').attr('name');

	ajax(url_etude,csrftoken,id_parent,type_parent);

});


// Fonction -----------------------------------------------------------------------------
//---------------------------------------------------------------------------------------

function effaceinfo() {
	$('#message').text("");

}

function ajaxOnClick(){
	console.log('ici')
	var url_etude = "/admin_page/userAuth/delete";

	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
	var id_parent = $('button[name="clikable"]').parent('td').attr('value');
	var type_parent = $('button[name="clikable"]').parent('td').attr('name');

	ajax(url_etude,csrftoken,id_parent,type_parent);
	$('button[name="del_etudeetape"]').on("click", ajaxOnClick);
}

function ajax(url_etude,csrftoken,id_parent,type_parent){
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
		url : url_etude,
		data : {
			val_user : id_parent,
			type_tab : type_parent,
		},
		type : 'POST',
		success: function(response, status, XHR){
			console.log("SUCCESS");

		}
	})

}