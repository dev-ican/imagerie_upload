$('select[name="select_etude"]').change(function(event) {
	var url_etude = "/admin_page/upfiles/tris/"
	var id_etude = $(this).children("option:selected").val();
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

$('td[class="clickable"]').one("click", function(){
	
	var url_etude = "/admin_page/upfiles/mod";
	var value = $(this).attr('value');
	var value_id = $(this).attr('name');

	var list = $("select[name='select_etude'] option:selected").val();
	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
	var td_parent = $( "td.clickable" ).parent('tr').attr('value');
	var var_modif = 'modif_' + td_parent + value

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
			value_id : value_id,
		},
		type : 'POST',
		success: function(response, status, XHR){
			console.log("SUCCESS");}
	}).done(function(data) {
		var val_data = JSON.parse(data);
		var count = Object.keys(val_data).length;
		var list_json = Object.values(val_data);
		var str_select = '<select class="custom-select mr-sm-2" name="list_etat" id="FormCustom">'

		for (let i=0;i < count; i++){
			if (Object.values(val_data)[i].nom == value_id){
				str_select = str_select + '<option value="' + Object.values(val_data)[i].id + '" selected>' + Object.values(val_data)[i].nom + '</option>'
			} else {
				str_select = str_select + '<option value="' + Object.values(val_data)[i].id + '">' + Object.values(val_data)[i].nom + '</option>'
			}
		}
		console.log(var_modif)
		document.getElementById(var_modif).innerHTML = str_select;
		document.getElementById(var_modif).className += "_select";
		$('td[class="clickable_select"]').off('click');
		document.getElementById('FormCustom').addEventListener("change", change_etat);
		console.log(str_select);
	})
});


// Fonction -----------------------------------------------------------------------------
//---------------------------------------------------------------------------------------

function change_etat(event) {
	var url_etude = "/admin_page/upfiles/maj";
	var etat_id = $(this).children("option:selected").val();
	var jonction_id = $(this).parent('td').attr('value');
	var value_etude = $('select[name="select_etude"]').children("option:selected").val();

	console.log(etat_id,'+++++++++', jonction_id);

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
			etat_id : etat_id,
			jonction : jonction_id,
			etude_id : value_etude
		},
		type : 'GET',
		success: function(response, status, XHR){
			console.log("SUCCESS");
			$('#ajax').html(response);}
	})
};