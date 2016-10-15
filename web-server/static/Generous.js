//add document ready 
$(document).ready(function(){
	google.charts.load('current', {packages: ['corechart', 'bar', 'table']});
	google.charts.setOnLoadCallback(drawTable);
	google.charts.setOnLoadCallback(drawBarChart);
	function drawBarChart(){
		var apiData = getGData(1);
		var data = google.visualization.arrayToDataTable(apiData);
		var view = new google.visualization.DataView(data);
		
		var options = {
			title: "Most Generous Employees",
			hAxis: {
				title: "Name"
				
				
			},
			vAxis:{
				title: 'Points'
				
			},
			legend: { position: "none" }
			
			
		}
		
		var chart = new google.visualization.ColumnChart(document.getElementById('nicedogsgraph'));
		chart.draw(data,options);
		
		
		
		
	}
	function drawTable(){
		var gData = new google.visualization.DataTable(0);
			gData.addColumn('number', 'Rank');
			gData.addColumn('string', 'Name');
			gData.addColumn('number', 'Awards Given');
			
			
			//perform api call to get Data
			var tablegData = getGData(0);
			gData.addRows(tablegData);
		
		var table = new google.visualization.Table(document.getElementById('nicedogs'));
		table.draw(gData, {showRowNumber: false, width: '100%', height: '100%'});
		
	}
	function getGData(choice){
		var returngData;
		//ordered data with rank for table chart
		if(choice === 0){
			returngData = [
			  [1,'Mike', 500 ],
			  [2,'Jim', 400],
			  [3,'Alice', 300],
			  [4,'Bob', 200]
			];
		}
		//data for bar graph
		else{
			returngData = [
				['Name', 'Points', {role: 'style'}],
				['Jazz', 500, 'gold'],
				['Rock', 400, 'silver'],
				['Pop', 300, 'orange'],
				['Rap', 200, 'black']
			];
		}
		return returngData;
	}
});
