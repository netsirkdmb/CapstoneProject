/**********************************************************************************************************************
** File Name: TopPerformers.js
** Author: Bryant Hall
** Description: Contains all the jquery and js and to pull data for table for google charts from our database; 
**
*********************************************************************************************************************/
//Begin loading when document is ready
$(document).ready(function(){
	//Load apis needed for this chart
	google.charts.load('current', {packages: ['corechart', 'bar', 'table' , 'controls']});
	google.charts.setOnLoadCallback(drawDashBoard);

	function drawDashBoard(){


		//Create a dashboard
		var dashBoard = new google.visualization.Dashboard(document.getElementById('topdogsdash'));
		
		//get data from server
		var jsonData =  JSON.parse($.ajax({
			url: "/admin/api/getRanking", 
			data: "json",
			async: false}).responseText);

		
		var trimmedResults = jsonData.Results.slice(0,5);
		var annualData = $.ajax({
			url: "/admin/api/getTopEmployees",
			data: "json",
			async: false

		}).responseText;

		console.log(trimmedResults);
		console.log(annualData);
		//create data table
		 var data = new google.visualization.arrayToDataTable(
			
[
			
                	['Name', 'Points', 'Month', {role: 'style'}],
                        ['Mike', 500, 1, 'gold'],
                        ['Jim', 400, 1, 'silver'],
                        ['Alice', 300, 1, 'orange'],
                        ['Bob', 200, 1 ,  'black'],
                        ['Mike', 800,2, 'gold'],
                        ['Jim', 500, 2, 'silver'],
                        ['Alice', 400, 2, 'orange'],
                        ['Bob', 250, 2 ,  'black']


                        ]

		);

		//create a control  wrapper for data
		
		 var controlWrapper = new google.visualization.ControlWrapper({
			'controlType': 'CategoryFilter',
			'containerId': 'filter_div',
			'options': {
				'filterColumnLabel': 'Month',
				'ui': {'allowMultiple': false}
			}


	  	 });
		//create data table
		var dataTable = new google.visualization.ChartWrapper({
			'chartType': 'Table',
			'containerId': 'topdogs',			
			'options': {
				'showRowNumber': false,
				'width': '100%',
				'height': '100%'
			}
			
		});


	
		//create bar chart
		var barChart = new google.visualization.ChartWrapper({
			'chartType': 'ColumnChart',
			'containerId': 'topdogsbar',
			'options' : {
                        	'title': "Employee Rankings",
                        	'hAxis': {
                                'title': "name"
                       		 },
                       		'vAxis':{
                                	'title': 'Points'
                        	},
                       		'legend': {'position': "none" }
                	}
		});

		//bind the dashboard with the controls and barchart				
		dashBoard.bind(controlWrapper   ,  [dataTable, barChart]);

		//bind the dashboard with the controls
		dashBoard.draw(data);


	

	}

});
