$(document).ready(function(){
	$("#searchbutton").click(function(){
		google.charts.load('current', {packages: ['corechart', 'bar', 'table']});
		
		var searchIndex = $("#ename").val();
		
		//check valid name, if valid begin querying for data
		
			//valid name
			$("#employeename").text("Employee Name: " + searchIndex);
			$("#Employee_rating").text("Overall Ranking: 25" );
			$("#awards_title").show();
		//Recieved awards
		google.charts.setOnLoadCallback(loadindiLineRecieved);
		google.charts.setOnLoadCallback(loadIndiPieRecieved);
		google.charts.setOnLoadCallback(getRecievedTransactions);
		google.charts.setOnLoadCallback(indiBarGiven);
		google.charts.setOnLoadCallback(indiPieGiven);
		google.charts.setOnLoadCallback(indiTableGiven);
		//Given Awards
		$("#given_title").show();
		
		//alert($("#ename").val());
		
		
	});
	function indiTableGiven(){
		var inputData = [
		["From", "Award Type", "Date"],
		["Kat", "Gold Star", "8/17/2015"],
		["Joan", "Silver Star", "8/30/2016"],
		["Marianne", "Bronze", "8/12/2012"]
		];
		
		var data = google.visualization.arrayToDataTable(inputData);
		var options={
			showRowNumber: false
			
		};
		
		var chart = new google.visualization.Table(document.getElementById('indiTableGiven'));
		chart.draw(data,options);
		
		
	};
	
	
	function indiPieGiven(){
		var inputData = [
			["Type", "Quantity"],
			["Above and Beyond Gold", 1],
			["Above and Beyond Silver", 4],
			["Above and Beyond Bronze", 30],
			];
		
		var data = google.visualization.arrayToDataTable(inputData);
		
		var options = {
			title: "Type of Awards Given"
			
		};
		var chart = new google.visualization.PieChart(document.getElementById('indiPieGiven'));
		chart.draw(data,options);
	};
	
	function indiBarGiven(){
		
		var inputData = [
				['Month', 'Awards Given'],
				['January', 10],
				['Febuary', 5],
				['March', 9],
				['April', 1]
			];
		
		var data = google.visualization.arrayToDataTable(inputData);
		
		var options = {
			title:"Awards Given Frequency",
			curveType: 'function',
			lengend: {position: 'bottom' }
		};
			
		
		
		var chart = new google.visualization.LineChart(document.getElementById('indiBarGiven'));
		chart.draw(data,options);
		
		
		
	};
	
	
	//Line chart showing points history
	function loadindiLineRecieved(searchIndex){
		var inputData = [
		['Month', 'Awards Given'],
          ['January', 1000],
          ['Febuary', 600],
          ['March', 900],
          ['April', 1200]
        ];
		var data = google.visualization.arrayToDataTable(inputData);
		
		
		var options = {
			title:"Award Frequency",
			curveType: 'function',
			lengend: {position: 'bottom' }
		};
		
			
			
		
		
		
		var chart = new google.visualization.LineChart(document.getElementById('indiLineRecieved'));
		chart.draw(data,options);
		//alert("Chart");
		
	};
	
	
	function loadIndiPieRecieved(){
		var inputData = [
			["Type", "Quantity"],
			["Above and Beyond Gold", 1],
			["Above and Beyond Silver", 4],
			["Above and Beyond Bronze", 30],
			];
		
		var data = google.visualization.arrayToDataTable(inputData);
		
		var options = {
			title:"Types of Award Breakdown"
			
		};
		var chart = new google.visualization.PieChart(document.getElementById('indiPieRecieved'));
		chart.draw(data,options);
		
	}
	
	function getRecievedTransactions(){
		var inputData = [
		["From", "Award Type", "Date"],
		["Kat", "Gold Star", "8/17/2015"],
		["Joan", "Silver Star", "8/30/2016"],
		["Marianne", "Bronze", "8/12/2012"]
		];
		var data = google.visualization.arrayToDataTable(inputData);
		var options = {
			showRowNumber: false
			
		};
		
		var resultTable = new google.visualization.Table(document.getElementById('indiTableRecieved'));
		resultTable.draw(data,options);
		
	};
	
	
	function getData(){
		
		
		
	};
});
