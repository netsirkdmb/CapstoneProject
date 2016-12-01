//Javascript and Jquery for chart award data. 

$(document).ready(function(){
	google.charts.setOnLoadCallback(drawTotals);
	google.charts.setOnLoadCallback(drawTotalsPie);
	
	function drawTotals(){
		var freqData = JSON.parse($.ajax({
			url: "/admin/api/getFrequencyChart",
			data: "json",
			async: false

		}).responseText);

		//format Data into google array format
		var formattedData = [["Date", "Quantity"]];
		for(var entry in freqData.Results){
			var newEntry =[];
			newEntry.push(freqData.Results[entry].month + " " +  freqData.Results[entry].year);
			newEntry.push(freqData.Results[entry].frequency);
			formattedData.push(newEntry);

		}
		formattedData = google.visualization.arrayToDataTable(formattedData);


		var options = {
			title:"Award Frequency",
			curveType: 'function',
			legend: {position: 'bottom' },
			width:500 ,
			height:400
		};
		
		var chart = new google.visualization.LineChart(document.getElementById('awardsfrequency'));
		chart.draw(formattedData,options);
		
		
		
		
	};
	
	function drawTotalsPie(){
		var totalsPieData = JSON.parse($.ajax({
			url: "/admin/api/getAwardTypes",
			data: "json",
			async: false

		}).responseText);
		//format data
		var formattedData=[['Type', 'Quantity']];
		for(var entry in totalsPieData.Results){
			var newEntry = [];
			newEntry.push(totalsPieData.Results[entry].name);
			newEntry.push(totalsPieData.Results[entry].frequency);
			formattedData.push(newEntry);
		
		}
		formattedData = google.visualization.arrayToDataTable(formattedData);
		var options = {
			title: "Award Types"
		};
		var chart = new google.visualization.PieChart(document.getElementById('PieBreakdown'));
		chart.draw(formattedData,options);
	}
	
	
});
