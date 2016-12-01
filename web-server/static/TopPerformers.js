/**********************************************************************************************************************
** File Name: TopPerformers.js
** Author: Bryant Hall
** Description: Contains all the jquery and js and to pull data for table for google charts from our database; 
**
*********************************************************************************************************************/
//Begin loading when document is ready
$(document).ready(function(){
	//Load apis needed for this chart
	google.charts.load('current', {packages: ['corechart',  'table' , 'controls']});
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
		var annualData = JSON.parse($.ajax({
			url: "/admin/api/getTopEmployees",
			data: "json",
			async: false

		}).responseText);

		var chartData = [
				['Name', 'Points', 'Month']
		];

		//Process the data in a datatable
		for (var entry in annualData.Results){
			for(var point in annualData.Results[entry]){
				var newEntry = [];
				if( annualData.Results[entry][point].name != undefined){
					newEntry.push(annualData.Results[entry][point].name);
					newEntry.push(annualData.Results[entry][point].points);
					//check if entry is a year, push 
					if(entry == 'Year')
						newEntry.push('Past Year');
					else{
						var month = entry.split('-');
						newEntry.push(month[0]);						
					}
					chartData.push(newEntry);
				}
			}		
		}

		//create data table
		 var data = new google.visualization.arrayToDataTable(
			chartData			
		);

		//create a control  wrapper for data
		 var controlWrapper = new google.visualization.ControlWrapper({
			'controlType': 'CategoryFilter',
			'containerId': 'filter_div',
			'options': {
				'filterColumnLabel': 'Month',
				'ui': {
					'allowMultiple': false,
					'allowNone': false
				}
			},
			'state' : {'selectedValues': ['All Time']}

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
                	},
			'view' : {'columns': [0,1]} 
		});

		//bind the dashboard with the controls and barchart				
		dashBoard.bind(controlWrapper   ,  [dataTable, barChart]);

		//bind the dashboard with the controls
		dashBoard.draw(data);
	}
});
