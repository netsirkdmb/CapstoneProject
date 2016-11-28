var userID=0;

$(document).ready(function(){
	$("#searchbutton").click(function(){
		google.charts.load('current', {packages: ['corechart', 'bar', 'table']});
		
		var searchIndex = $("#ename").val();
		//check valid email, if valid begin querying for data
		$.ajax({
			url: "/admin/API/getUserByEmail",
			data: "json",
			method: "POST",
			data: { "email": searchIndex}	
		


		}).done(function(result){
			 //valid name
			if(result.ID >0){
				userID = result.ID;			     
        		        $("#employeename").text("Employee Name: " + searchIndex);
		                //get employee rating
				
				$.ajax({
					url: "/admin/API/getRanking/" + userID,
					data: "json"							
				})
				.done(function(ranking){
					ranking = JSON.parse(ranking);
					$("#Employee_rating").text("Overall Ranking: " + ranking.Results[0].rank );
			
				});
				
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



			}		
			else{
				alert("Invalid Username.");
			}


		});
		
	});
	function indiTableGiven(){
		var targetUrl = '/admin/API/userAwards/' + userID;
		$.ajax({
			url: targetUrl,
			format:"json"
			
		})
		.done(function(returnData){
			var jsonData = JSON.parse(returnData);

			//format data
			var formattedData = [["To", "Type", "Date"]];
			for(var entry in jsonData.Data){
				var newEntry = [];
				newEntry.push(jsonData.Data[entry].receiverName);
				newEntry.push(jsonData.Data[entry].awardType);
				newEntry.push(jsonData.Data[entry].awardDate);
				formattedData.push(newEntry);

			} 
			//drawdata

			var data = google.visualization.arrayToDataTable(formattedData);
	                var options={
        	                showRowNumber: false
                	};

	                var chart = new google.visualization.Table(document.getElementById('indiTableGiven'));
        	        chart.draw(data,options);
		});
	};
	
	
	function indiPieGiven(){
		$.ajax({
			url:'/admin/API/getAwardTypesGiven/' + userID,
			format:"json"

		})
		.done(function(data){
			//console.log(data);
			//format data



			 var jsonData = JSON.parse(data);

                        //format data
                        var formattedData = [["Type", "Quantity"]];
                        for(var entry in jsonData.Data){
                                var newEntry = [];
                                newEntry.push(jsonData.Data[entry].type);
                                newEntry.push(jsonData.Data[entry].frequency);
                                formattedData.push(newEntry);

                        }

                        console.log(formattedData);
	                formattedData = google.visualization.arrayToDataTable(formattedData);

        	        var options = {
                	        title: "Type of Awards Given"

	                };
        	        var chart = new google.visualization.PieChart(document.getElementById('indiPieGiven'));
                	chart.draw(formattedData,options);
		});
	};
	
	function indiBarGiven(){
		
		$.ajax({
			url: '/admin/API/getAwardsGivenFrequency/' + userID,
			format: "json"

		})
		.done(function(data){
			//format data
			 var jsonData = JSON.parse(data);

                        //format data
                        var formattedData = [["Date", "Number of Awards Given"]];
                        for(var entry in jsonData.Data){
                                var newEntry = [];
                                newEntry.push(jsonData.Data[entry].month + ' ' + jsonData.Data[entry].year);
                                newEntry.push(jsonData.Data[entry].frequency);
                                formattedData.push(newEntry);

                        }

                        formattedData = google.visualization.arrayToDataTable(formattedData);
			var options = {
                        	title:"Awards Given Frequency",
        	                legend: {position: 'bottom' },
				width: 500,
				height: 400,
				viewWindowMode: 'explicit',
				vAxis: {minValue: 0}			
                	};



	                var chart = new google.visualization.LineChart(document.getElementById('indiBarGiven'));
        	        chart.draw(formattedData,options);
		});
	};
	
	
	//Line chart showing points history
	function loadindiLineRecieved(searchIndex){
		$.ajax({
			url:'/admin/API/getPrestigePoints/' + userID,
			format: 'json'

		})
		.done(function(data){
                        //format data
                         var jsonData = JSON.parse(data);

                        //format data
                        var formattedData = [["Date", "Number of Awards Given"]];
                        for(var entry in jsonData.Results){
                                var newEntry = [];
                                newEntry.push(jsonData.Results[entry].month + ' ' + jsonData.Results[entry].year);
                                newEntry.push(jsonData.Results[entry].points);
                                formattedData.push(newEntry);

                        }

                        formattedData = google.visualization.arrayToDataTable(formattedData);
			var options = {
	                        title:"Awards Recieved Value",
	                        legend: {position: 'bottom' },
				width: 500,
				height: 400
        	        };

	                var chart = new google.visualization.LineChart(document.getElementById('indiLineRecieved'));
        	        chart.draw(formattedData,options);

		});
	};
	
	
	function loadIndiPieRecieved(){
		$.ajax({
			url: "/admin/API/getAwardTypes/" + userID,
			format: "json"

		}).
		done(function(data){
			var jsonData = JSON.parse(data);

                        //format data
                        var formattedData = [["Date", "Number of Awards Given"]];
                        for(var entry in jsonData.Results){
                                var newEntry = [];
                                newEntry.push(jsonData.Results[entry].name);
                                newEntry.push(jsonData.Results[entry].frequency);
                                formattedData.push(newEntry);

                        }

                        formattedData = google.visualization.arrayToDataTable(formattedData);
	                var options = {
        	                title:"Types of Award Breakdown"
                	};

	                var chart = new google.visualization.PieChart(document.getElementById('indiPieRecieved'));
        	        chart.draw(formattedData,options);
		});


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
		$.ajax({
			url:"/admin/API/getAwardsRecieved/" + userID,
			format:"json"	

		}).done(function(data){
			console.log(data);

			var jsonData = JSON.parse(data);

                        //format data
                        var formattedData = [["From", "Award Type", "Date"]];
                        for(var entry in jsonData.Data){
                                var newEntry = [];
                                newEntry.push(jsonData.Data[entry].giverName);
                                newEntry.push(jsonData.Data[entry].awardType);
                                newEntry.push(jsonData.Data[entry].awardDate);
                                formattedData.push(newEntry);

                        }

                        console.log(formattedData);
                        formattedData = google.visualization.arrayToDataTable(formattedData);
	                var options = {
        	                showRowNumber: false

                	};
	
        	        var resultTable = new google.visualization.Table(document.getElementById('indiTableRecieved'));
                	resultTable.draw(formattedData,options);




		});

		
	};
	
	
	function getData(){
		
		
		
	};
});
