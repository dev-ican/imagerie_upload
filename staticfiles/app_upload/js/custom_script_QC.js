$('td[class="click_qc"]').one("click", function(){
	
	var url_etude = "/admin_page/upfiles/modQC";
	var dossier_upload_id = $(this).attr('name');
	var suivi_upload_id = $(this).parent('tr').attr('value');
	console.log(dossier_upload_id, suivi_upload_id)

	// var list = $("select[name='select_etude'] option:selected").val();
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
			val_jonction : dossier_upload_id,
		},
		type : 'POST',
		success: function(response, status, XHR){
			console.log("SUCCESS");}
	}).done(function(data) {
		var val_data = JSON.parse(data);
		var count = Object.keys(val_data).length;
		var list_json = Object.values(val_data);
		var str_select = '<select class="custom-select mr-sm-2" name="select_qc" id="FormQC">'

		for (let i=0;i < count; i++){
			if (Object.values(val_data)[i].nom == dossier_upload_id){
				str_select = str_select + '<option value="' + Object.values(val_data)[i].id + '" selected>' + Object.values(val_data)[i].nom + '</option>'
			} else {
				str_select = str_select + '<option value="' + Object.values(val_data)[i].id + '">' + Object.values(val_data)[i].nom + '</option>'
			}
		}
		var_name = 'qc_mod_' + dossier_upload_id + suivi_upload_id

		console.log("var_name : " + var_name)
		console.log("str_select : " + str_select)

		document.getElementById(var_name).innerHTML = str_select;
		document.getElementById(var_name).className += "_select";
		$('td[class="clickable_select"]').off('click');
		document.getElementById('FormQC').addEventListener("change", change_qc);
	})
});


// Fonction -----------------------------------------------------------------------------
//---------------------------------------------------------------------------------------

function change_qc(event) {
	let suppr_data = false
	let accept_QC_RGPD = false
	var url_etude = "/admin_page/upfiles/majQC";
	var etat_id = $(this).children("option:selected").val();
	var dossier_upload_id = $(this).parent('td').attr('name');
	var value_etude = $('select[name="etude_choice"]').children("option:selected").val();
	var value_centre = $('select[name="centre_choice"]').children("option:selected").val();
	const url_research = "/admin_page/upfiles/"

	var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};
	
	if (etat_id === '4') {
		accept_QC_RGPD = confirm("En indiquant un manquement RGPD, toutes les données associées seront supprimées.");
		accept_QC_RGPD ? suppr_data = true : suppr_data = false; 
	} else {
		accept_QC_RGPD = true;
		suppr_data = false;
	};

	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
	if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
	});

	console.log("accept_QC_RGPD :" + accept_QC_RGPD, "suppr_data :" + suppr_data);

	if (accept_QC_RGPD) {
		$.ajax({
			url : url_etude + "/",
			data : {
				etat_id : etat_id,
				dossier_upload_id : dossier_upload_id,
				etude_id : value_etude,
				centre_id : value_centre,
				data_suppr : suppr_data
			},
			type : 'GET',
			success: function(response, status, XHR){
				console.log("SUCCESS");
				console.log(response);
				$('#ajax').html(response);
				// $('body').load(url_research, function(response, status, XHR){});
				location.reload();
			}
		})
	} else {
		// $('body').load(url_research, function(response, status, XHR){})
		location.reload();
	};
};