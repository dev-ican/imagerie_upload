$('a[id="walk_dir"]').click(function(event) {
	var url_walk = "/admin_page/upfiles/walk_up/"
	var id_etude = $('a[id="id_etude"]').attr('name');
	var walk_url = $(this).attr('name');
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
		url : url_walk,
		data : {
			url : walk_url,
			id_etude : id_etude
		},
		type : 'GET',
		success: function(response, status, XHR){
			console.log("SUCCESS");}
	}).done(function(data) {
		var val_data = JSON.parse(data);
		var count = Object.keys(val_data).length;
		var list_json = Object.values(val_data);
		str_select = '<tr><td><a id="walk_return" name="' + Object.values(val_data)[0].url + '">...</a></td></tr>'
		for (let i=0;i < count; i++){
			if (Object.values(val_data)[i].dir == true){
				str_select += '<tr><td><a name="' + Object.values(val_data)[i].url + 'id="walk_dir">Dossier : ' + Object.values(val_data)[i].nom + '</a></td><td>Nombre de fichiers ' + Object.values(val_data)[i].x + '</td><td>Nombre de dossiers ' + Object.values(val_data)[i].y + '</td></tr>';
			} else {
				str_select += '<tr><td>' + Object.values(val_data)[i].nom + '</td><td><a href="/admin_page/upfiles/downOnce/' + Object.values(val_data)[i].url + '"><span button type="button" class="btn btn-primary">Télécharger</span></a></td></tr>';
			}
		}
		console.log(str_select)
		document.getElementById('walk_tab').innerHTML = str_select;
		document.getElementById('walk_return').addEventListener("click",click_retour);
	})
});

function click_retour(event) {
	var url_walk = "/admin_page/upfiles/walk_return/";
	var id_etude = $('a[id="id_etude"]').attr('name');
	var walk_url = $('a[id="walk_return"]').attr('name');
	var val_compare = $('td[id="value_nom"]').attr('name');
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
		url : url_walk,
		data : {
			url : walk_url,
			val_compare : val_compare,
			id_etude : id_etude
		},
		type : 'GET',
		success: function(response, status, XHR){
			console.log("SUCCESS");}
	}).done(function(data) {
		if (data){
		var val_data = JSON.parse(data);
		var count = Object.keys(val_data).length;
		var list_json = Object.values(val_data);
		console.log(data)

		str_select = '<tr><td><a id="walk_return" name="' + Object.values(val_data)[0].url + '">...</a></td></tr>'
		for (let i=0;i < count; i++){
			console.log(Object.values(val_data)[i].dir)
			if (Object.values(val_data)[i].dir == true){
				str_select += '<td><a name="' + Object.values(val_data)[i].url + 'id="walk_dir">Dossier : ' + Object.values(val_data)[i].nom + '</a></td><td>Nombre de fichiers ' + Object.values(val_data)[i].x + '</td><td>Nombre de dossiers ' + Object.values(val_data)[i].y + '</td></tr>';
			} else {
				str_select += '<tr><td>' + Object.values(val_data)[i].nom + '</td><td><a href="/admin_page/upfiles/downOnce/' + Object.values(val_data)[i].url + '"><span button type="button" class="btn btn-primary">Télécharger</span></a></td></tr>';
			}
			console.log(str_select)
		}
		document.getElementById('walk_tab').innerHTML = str_select;
		//$('tr[id="walk_tab"]').html(str_select);
	}
	})
};
