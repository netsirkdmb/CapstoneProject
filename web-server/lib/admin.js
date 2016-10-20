// Global Variable Decleration
var express = require('express'); 
var myRouter = express.Router(); 
var request = require('request');

/*****************************************************
		Login Routers 
*****************************************************/ 

//renders users page with dummy data 
myRouter.get('/users' , function (req,res){
	//get data from server here in future
	var context = {};
	var results=[];  //used to store processed results from server

	//send out request to server to get data needed for current admins
	request('http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/users', function(err, response,body){
		//convert response to JSON and process it
		var jsonResult = JSON.parse(body);
	
		//go through every result in JSON data and append to a results array. 
		for(var entry in jsonResult.Data){
			results.push({
				name: jsonResult.Data[entry][2],
				email: jsonResult.Data[entry][3],
				password: jsonResult.Data[entry][4],
				time: jsonResult.Data[entry][5],
				image: jsonResult.Data[entry][4],
				region: jsonResult.Data[entry][6]		
			}
			);
		}

		//send data to be rendered
		context.data = results;
		res.render('admin/users', context);
	}
	);
});

//renders admin page with dummy data 
myRouter.get('/admins', function(req,res){
	//get data from server here
	var context = {};
	 var results=[];  //used to store processed results from server

        //send out request to server to get data needed for current admins
        request('http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins', function(err, response,body){
                //convert response to JSON and process it
                var jsonResult = JSON.parse(body);
		console.log(body);

                //go through every result in JSON data and append to a results array.
                for(var entry in jsonResult.Data){
                        results.push({
                                name: jsonResult.Data[entry][1],
                                email: jsonResult.Data[entry][2],
                                password: jsonResult.Data[entry][3],
                                time: "Coming Soon"
                        }
                        );
                }

                //send data to be rendered
                context.data = results;
		res.render('admin/admins', context);
        
        }
        );


	context.data = [
		{name:"bob", email:"yomommasofat", password:"1", time: "8:00am"},
		{name:"bob1", email:"yomommasofat1", password:"12", time: "8:01am"},
		{name:"bob2", email:"yomommasofat2", password:"123", time: "8:02am"}
	];
});

//renders business intelligence page 
myRouter.get('/bi', function(req,res){
	res.render('admin/bi');
});

//allow the router to be exported 
module.exports = myRouter;
