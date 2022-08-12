$('button[name="supprEtudeAuth"]').on("click", function(){
	var url_etude = "/admin_page/userAuth/delete";
	var id_ = $(this).attr('value');

	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
	var id_parent = $('button[name="supprEtudeAuth"]').parent('td').attr('value');
	var type_parent = $('button[name="supprEtudeAuth"]').parent('td').attr('name');

	ajax(url_etude,id_,csrftoken,id_parent,type_parent);

});


// Fonction -----------------------------------------------------------------------------
//---------------------------------------------------------------------------------------

function effaceinfo() {
	$('#message').text("");

}

function ajaxOnClick(){
	console.log('ici')
	var url_etude = "/admin_page/userAuth/delete";
	var id_ = $(this).attr('value');

	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
	var id_parent = $('button[name="supprEtudeAuth"]').parent('td').attr('value');
	var type_parent = $('button[name="supprEtudeAuth"]').parent('td').attr('name');

	ajax(url_etude,id_,csrftoken,id_parent,type_parent);
	$('button[name="supprEtudeAuth"]').on("click", ajaxOnClick);
}

function ajax(url_etude,id_,csrftoken,id_parent,type_parent){
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
			val_id : id_,
			val_user : id_parent,
			type_tab : type_parent,
		},
		type : 'POST',
		success: function(response, status, XHR){
			console.log("SUCCESS");
			// console.log(response);
			var val_data = JSON.parse(response);
			var str_etude = "";
			var tab_var = 0;
			var y = 0;
			var count = Object.keys(val_data).length;

			for (let x=0; x < count; x++){

				if (x == 0){
					tab_var = Object.values(val_data)[x];
					y = 0
					for (const property in tab_var) {
  						y += 1;
					}
				for (let i=0;i < y; i++){
					str_etude = str_etude + '<tr><td>' + Object.values(val_data)[x][i].nom + '</td><td>' + Object.values(val_data)[x][i].date + '</td>'
					str_etude = str_etude + '<td value="' + Object.values(val_data)[x][i].id_user + '" name="etude"><button role="button" class="btn btn-sm btn-outline-secondary" name="clikable" value="' + Object.values(val_data)[x][i].id_jonc + '">'
					str_etude = str_etude + "Supprimer l'attribution</button></td></tr>"
				}
				} else if (x == 1) {
					tab_var = Object.values(val_data)[x];
					y = 0
					for (const property in tab_var) {
  						y += 1;
					}
				for (let i=0;i < y; i++){
					str_centre = '<tr><td>' + Object.values(val_data)[x][i].nom + '</td><td>' + Object.values(val_data)[x][i].num + '</td><td>' + Object.values(val_data)[x][i].date + '</td>'
					str_centre = str_centre + '<td value="' + Object.values(val_data)[x][i].id_user + '" name="centre"><button role="button" class="btn btn-sm btn-outline-secondary" name="clikable" value="' + Object.values(val_data)[x][i].id_jonc + '">'
					str_centre = str_centre + "Supprimer l'attribution</button></td></tr>"
				}
				}
			}

			$('#etude_tab').html(str_etude);
			$('#centre_tab').html(str_centre);
			$('#message').text(Object.values(val_data)[2]);
			x = setTimeout(effaceinfo, 2000);
			$('button[name="clikable"]').on("click", ajaxOnClick);
		}
	})

}