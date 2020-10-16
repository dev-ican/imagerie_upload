var ctx = document.getElementById('myChart').getContext('2d');

var data_etude = $('#myChart').attr('value');
const tab_etude = data_etude.split(',');

for (var x = 0; i < tab_etude.length; i++){
	tab_etude[x].replace("['", "");
	tab_etude[x].replace("]", "");
	tab_etude[x].replace("'", "");
	tab_etude[x].replace(" ", "");

}

var list_etude = new Array();
var list_etude_data = new Array();

console.log(tab_etude)
var coupe = 0;
for (var i = 0; i < data_etude.length; i++) {
		if (data_etude[i] != 'data' && data_etude[i] == 0){
		list_etude.push(data_etude[i])
	}else if (data_etude[i] != 'data' && data_etude[i] == 1){
		list_etude_data.push(data_etude[i])
	}else if (data_etude[i] == 'data'){
		coupe += 1
	}
}

console.log(list_etude)

var myChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});

