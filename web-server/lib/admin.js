// Global Variable Decleration
var express = require('express'); 
var myRouter = express.Router(); 
var request = require('request');
var uuid = require('node-uuid');

/*****************************************************
		Login Routers 
*****************************************************/ 

//renders users page with dummy data 
myRouter.get('/admin/users' , function (req,res){
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
				
				uid: jsonResult.Data[entry].userID,
				uuid: jsonResult.Data[entry].uuID,
				name: jsonResult.Data[entry].name,
				email: jsonResult.Data[entry].email,
				password: jsonResult.Data[entry].password,
				time: jsonResult.Data[entry],
				image: jsonResult.Data[entry].signatureImage,
				region: jsonResult.Data[entry].region		
						
				}
			);
		}

		console.log("JSON to render for user page: " + results);

		//send data to be rendered
		context.data = results;
		res.render('admin/users', context);
	}
	);
});


//renders admin page with dummy data 
myRouter.get('/admin/admins', function(req,res){
	
	//get data from server here
	var context = {};
	 var results=[];  //used to store processed results from server

        //send out request to server to get data needed for current admins
        request('http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins', function(err, response,body){
                //convert response to JSON and process it
                var jsonResult = JSON.parse(body);

                //go through every result in JSON data and append to a results array.
                for(var entry in jsonResult.Data){
                        results.push({
				uuid: jsonResult.Data[entry].uuID,
                                id: jsonResult.Data[entry].adminID,
                                email: jsonResult.Data[entry].email,
                                password: jsonResult.Data[entry].password,
                                time: "Coming Soon"
                        }
                        );
                }

                //send data to be rendered
                context.data = results;
		res.render('admin/admins', context);
        
        }
        );
});

//renders business intelligence page 
myRouter.get('/admin/bi', function(req,res){
	res.render('admin/bi');
});


/**********************************************************************************************************
API LINKS
-Handles Crud Requests from user
**********************************************************************************************************/


//Handle Remove Create and Update Operations Here. Take data from site and redirect to Database server

myRouter.route('/admin/API/admin').post(
		 function(req,res){
		
		var values =  {password: req.body.password, email:  req.body.email, uuID:  uuid.v4() };
		console.log("Post Values");
		request.post({url: 'http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins', form: values }, function(err, response,body){
		        if(!err && response.statusCode < 400){
                                res.send("1");
                        }
                        else{
				console.log("ERROR");
                                if(response)
                                        console.log(err);
                                console.log(response);
				res.send("0");
                        }
		});		
	});
myRouter.route('/admin/API/admin/:uuID')
	.put(function(req,res){
		var values =  {password: req.body.password, email:  req.body.email, uuID:  req.body.uuid };

	        request.put({url:'http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins/' + req.params.uuID, form:values}, function(err, response,body){
                        if(!err && response.statusCode < 400){
                                res.send("1");
                        }
                        else{
                                if(response)
                                        console.log(err);
                                console.log(response.body);
                                res.send("0");
                        }
                });

	})
	.delete(function(req,res){
		console.log("Delete Request for ID: " + req.params.ID);
		request.delete('http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins/' + req.params.uuID, function(err, response,body){
			console.log(req.session);
			if(!err && response.statusCode < 400){
				res.send("1");
			}
			else{
				console.log("ERRROR!!!!");
				if(response)
					console.log(err);
				console.log(response);
				res.send("0");	
			}
		});
});



/****************************************************************************************************************************************
**							USERS
**
*****************************************************************************************************************************************/


//Handle Remove Create and Update Operations Here. Take data from site and redirect to Database server

myRouter.route('/admin/API/user')
        //create New Router
        .post( function(req,res){

                var values =  {password: req.body.password, email:  req.body.email, uuID: uuid.v4()  , region: req.body.region, signatureImage: "comingsoon", name: req.body.name };
                console.log(values);
                request.post({url: 'http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/users', form: values }, function(err, response,body){
                        if(!err && response.statusCode < 400){
                                console.log(JSON.stringify(body));
                                res.send("1");
                        }
                        else{
                                if(response)
                                        console.log(err);
                                console.log(response);
                                res.send("0");
                        }
                });
        });
myRouter.route('/admin/API/user/:ID')
        .put(function(req,res){
                console.log("Update Request for ID: " + req.params.ID);
		var values =  {password: req.body.password, email:  req.body.email,  region: req.body.region, signatureImage: "comingsoon", name: req.body.name };
                console.log(values);
		request.put({url:'http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/users/' + req.params.ID, form: values}, function(err, response,body){
                        if(!err && response.statusCode < 400){
                                console.log(body);
                                res.send("1");
                        }
                        else{
                                if(response)
                                        console.log(err);
                                console.log(response.body);
                                res.send("0");
                        }
                });

        })
        .delete(function(req,res){
                console.log("Delete Request for ID: " + req.params.ID);
                request.delete('http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/users/' + req.params.ID, function(err, response,body){
                        if(!err && response.statusCode < 400){
                                console.log(body);
                                res.send("1");
                        }
                        else{
                                if(response)
                                        console.log(err);
                                console.log(response);
                                res.send("0");
                        }
                });



	});







//allow the router to be exported 
module.exports = myRouter;
