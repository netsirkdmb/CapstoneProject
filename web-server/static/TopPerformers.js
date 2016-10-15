$(document).ready(function(){
	google.charts.load('current', {packages: ['corechart', 'bar', 'table']});
	//google.charts.load('current', {'packages':['table']});
	google.charts.setOnLoadCallback(drawTable);
	google.charts.setOnLoadCallback(drawBarChart);
	function drawTable(){
		var data = new google.visualization.DataTable();
			data.addColumn('number', 'Rank');
			data.addColumn('string', 'Name');
			data.addColumn('number', 'Points');
			data.addColumn('string', 'Region');
			
			//perform api call to get data
			var tableData = getData(1);
			data.addRows(tableData);
		
		var table = new google.visualization.Table(document.getElementById('topdogs'));
		table.draw(data, {showRowNumber: false, width: '100%', height: '100%'});
		
	}
	function drawBarChart (){
		var tableData = getData(0);
		//console.log(tableData);
		var data = google.visualization.arrayToDataTable(tableData);
		var view = new google.visualization.DataView(data);
		var options ={
			title: "Employee Rankings",
			hAxis: {
				title: "name"
				
				
			},
			vAxis:{
				title: 'Points'
				
			},
			legend: { position: "none" }
			
		};
		
		var chart = new google.visualization.ColumnChart(document.getElementById('topdogsbar'));
		chart.draw(data,options);
		
	}


	function getData(choice){
		var returnData =[];
		//data for table, include rank and region
		if(choice === 1 ){
			returnData = [
				  [1,'Mike', 500, "Seattle"],
				  [2,'Jim', 400, "Bellevue"],
				  [3,'Alice', 300, "Vancouver BC"],
				  [4,'Bob', 200, "San Diego"]
				];
		}
		//data for bar chart
		else{
			returnData = [
				  ['Name', 'Points', {role: 'style'}],
				  ['Mike', 500, 'gold'],
				  ['Jim', 400, 'silver'],
				  ['Alice', 300, 'orange'],
				  ['Bob', 200, 'black']
				];
		}
		return returnData;
		
		
		
		
	}
});
