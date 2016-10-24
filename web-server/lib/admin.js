// Global Variable Decleration
var express = require('express'); 
var myRouter = express.Router(); 
var request = require('request');

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
				uid: jsonResult.Data[entry][0],
				uuID: jsonResult.Data[entry][1],
				name: jsonResult.Data[entry][2],
				email: jsonResult.Data[entry][3],
				password: jsonResult.Data[entry][4],
				time: jsonResult.Data[entry][5],
				image: jsonResult.Data[entry][4],
				region: jsonResult.Data[entry][6]		
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
		console.log(body);

                //go through every result in JSON data and append to a results array.
                for(var entry in jsonResult.Data){
                        results.push({
				uid: jsonResult.Data[entry][0],
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

myRouter.route('/adminAPI/admin')
	//create New Router
	.post( function(req,res){
		
		var values =  {password: req.body.password, email:  req.body.email, uuID:  req.body.uuID };
		console.log(values);
		request.post({url: 'http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins', form: values }, function(err, response,body){
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
myRouter.route('/adminAPI/admin/:uuID')
	.put(function(req,res){
		console.log("Update Request for UUID: " + req.params.uuID); 
	        request.put('http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins/' + req.params.uuID, function(err, response,body){
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

	})
	.delete(function(req,res){
		console.log("Delete Request for UUID: " + req.params.uuID);
		request.delete('http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins/' + req.params.uuID, function(err, response,body){
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






//Handle Remove Create and Update Operations Here. Take data from site and redirect to Database server

myRouter.route('/adminAPI/user')
        //create New Router
        .post( function(req,res){

                var values =  {password: req.body.password, email:  req.body.email, uuID:  req.body.uuID, region: req.body.region, signatureImage: "comingsoon", name: req.body.name };
                console.log(values);
                request.post({url: 'http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/users', form: values }, function(err, response,body){
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
myRouter.route('/adminAPI/user/:uuID')
        .put(function(req,res){
                console.log("Update Request for UUID: " + req.params.uuID);
                request.put('http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/users/' + req.params.uuID, function(err, response,body){
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

        })
        .delete(function(req,res){
                console.log("Delete Request for UUID: " + req.params.uuID);
                request.delete('http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/users/' + req.params.uuID, function(err, response,body){
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
