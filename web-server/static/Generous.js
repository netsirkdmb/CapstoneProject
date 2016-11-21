//add document ready 
$(document).ready(function(){
	google.charts.load('current', {packages: ['corechart', 'bar', 'table' , 'controls']})
	google.charts.setOnLoadCallback(drawDashBoard);
	function drawDashBoard(){
		var dashBoard = new google.visualization.Dashboard(document.getElementById('nicedogsdash'));
		
		//get data from server

		var genData =JSON.parse($.ajax({
                        url: "/admin/api/getGenerousEmployees",
                        data: "json",
                        async: false
                }).responseText);
		
		//create data table
	        var chartData = 
		[
                        ['Name', 'Frequency', 'Month', {role: 'style'}]
		];
             

		/*        ['Mike', 500, 1, 'gold'],
                        ['Jim', 400, 1, 'silver'],
                        ['Alice', 300, 1, 'orange'],
                        ['Bob', 200, 1 ,  'black'],
                        ['Mike', 800,2, 'gold'],
                        ['Jim', 500, 2, 'silver'],
                        ['Alice', 400, 2, 'orange'],
                        ['Bob', 250, 2 ,  'black']


                        ]
*/
                



		for (var entry in genData.Results){
			for(var point in genData.Results[entry]){
                                var newEntry = [];
                                if( genData.Results[entry][point].name != undefined){
                                        newEntry.push(genData.Results[entry][point].name);
                                        newEntry.push(genData.Results[entry][point].frequency);
                                        if(entry == 'Year')

                                                newEntry.push(0);
                                        else
                                                if (point <10)
                                                        newEntry.push(parseInt(entry.substring(0,1)));
                                                else
                                                         newEntry.push(parseInt(entry.substring(0,2)))
						newEntry.push('gold');
                                        chartData.push(newEntry);
                                }
                        }
                }

		
		console.log(chartData);		

		data = new google.visualization.arrayToDataTable(chartData);



	
		//Control Wrapper

		var controlWrapper = new google.visualization.ControlWrapper({
		        'controlType': 'CategoryFilter',
                        'containerId': 'gen_Filter',
                        'options': {
                                'filterColumnLabel': 'Month',
                                'ui': {'allowMultiple': false}
                        }

	
		});

	
		//create bar chart
		var barChart = new google.visualization.ChartWrapper({
	        	'chartType': 'ColumnChart',
                        'containerId': 'nicedogsgraph',
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
			'view': {'columns': [0,1]}


		});

		//create visualization
		var dataTable = new google.visualization.ChartWrapper({
			'chartType': 'Table',
			'containerId': 'nicedogs',
			'options' :  {
                                'showRowNumber': false,
                                'width': '100%',
                                'height': '100%'
			}
		});
		
		//bind charts to dashboard
		dashBoard.bind(controlWrapper, [dataTable, barChart]); 

		//draw dashboard
		dashBoard.draw(data);

	};
});
/*
	function drawBarChart(){
		var apiData = getGData(1);
		var data = google.visualization.arrayToDataTable(apiData);
		var genData = $.ajax({
			url: "/admin/api/getGenerousEmployees",
			data: "json",
			async: false

		}).responseText; 		
	

		console.log("genData: " + genData); 
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
*/
