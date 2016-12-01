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
                        ['Name', 'Frequency', 'Month']
		];
             
		//Filter and Process the data in a array for ingenstion by google charts
		for (var entry in genData.Results){
			for(var point in genData.Results[entry]){
                                var newEntry = [];
                                if( genData.Results[entry][point].name != undefined){
                                        newEntry.push(genData.Results[entry][point].name);
                                        newEntry.push(genData.Results[entry][point].frequency);
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

		
		data = new google.visualization.arrayToDataTable(chartData);



	
		//Control Wrapper

		var controlWrapper = new google.visualization.ControlWrapper({
		        'controlType': 'CategoryFilter',
                        'containerId': 'gen_Filter',
                        'options': {
                                'filterColumnLabel': 'Month',
                                'ui': {
					'allowMultiple': false,
					'allowNone': false
				}
                        },
			'state': {'selectedValues': ['Past Year']}

	
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
                                        'title': 'Frequency'
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
