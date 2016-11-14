//Javascript and Jquery for chart award data. 

$(document).ready(function(){
	google.charts.setOnLoadCallback(drawTotals);
	google.charts.setOnLoadCallback(drawTotalsPie);
	
	function drawTotals(){
		var inputData = getData(0);
		var data = google.visualization.arrayToDataTable(inputData);
		var freqData = $.ajax({
			url: "/admin/api/getFrequencyChart",
			data: "json",
			async: false

		}).responseText;
		console.log("Freq Data: " + freqData);

		var options = {
			title:"Award Frequency",
			curveType: 'function',
			lengend: {position: 'bottom' }
		};
		
		var chart = new google.visualization.LineChart(document.getElementById('awardsfrequency'));
		chart.draw(data,options);
		
		
		
		
	};
	
	function drawTotalsPie(){
		var inputData = getData(1);
		var data = google.visualization.arrayToDataTable(inputData);
		var totalsPieData = $.ajax({
			url: "/admin/api/getAwardTypes",
			data: "json",
			async: false

		}).responseText;
		console.log("Totals Pie : " + totalsPieData);
		var options = {
			title: "Award Types"
		};
		var chart = new google.visualization.PieChart(document.getElementById('PieBreakdown'));
		chart.draw(data,options);
	}
	
	
	function getData(value){
		//Ajax call here
		var data;
		if(value === 0){
		
		//getData
		   data =	[
          ['Month', 'Awards Given'],
          ['January', 1000],
          ['Febuary', 600],
          ['March', 900],
          ['April', 1200]
        ];
		}
		else{
			data = [
			["Type", "Quantity"],
			["Above and Beyond Gold", 1],
			["Above and Beyond Silver", 4],
			["Above and Beyond Bronze", 30],
			];
			
		}
		return data;
		
		
	};
});
