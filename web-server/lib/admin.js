// Global Variable Decleration
var express = require('express'); 
var myRouter = express.Router(); 
var request = require('request');
var async = require('async');
var cryptoHash = require('./cryptoHash.js'); 
var multer  = require('multer')
var upload = multer({ dest: 'lib/uploads/' })
var fs = require('fs');
var FormData = require('form-data');
var serverPath = 'https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/'

//var serverPath = 'http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/'

/*****************************************************
		Login Routers 
*****************************************************/ 

//renders users page with dummy data 
myRouter.get('/admin/users' , function (req,res){
	//get data from server here in future
	var context = {};
	var results=[];  //used to store processed results from server

	//send out request to server to get data needed for current admins
	request(serverPath + 'users', function(err, response,body){
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
				time: jsonResult.Data[entry].accountCreationTime,
				startDate: jsonResult.Data[entry].startDate,
				region: jsonResult.Data[entry].region		
						
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
myRouter.get('/admin/admins', function(req,res){
	
	//get data from server here
	var context = {};
	 var results=[];  //used to store processed results from server

        //send out request to server to get data needed for current admins
        request(serverPath + 'admins', function(err, response,body){
                //convert response to JSON and process it
                var jsonResult = JSON.parse(body);

                //go through every result in JSON data and append to a results array.
                for(var entry in jsonResult.Data){
                        results.push({
				uuid: jsonResult.Data[entry].uuID,
                                id: jsonResult.Data[entry].adminID,
                                email: jsonResult.Data[entry].email,
                                password: jsonResult.Data[entry].password,
                                time: jsonResult.Data[entry].accountCreationTime
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

/***********************************************************************************************************************************
** API Call for Image
**********************************************************************************************************************************/
myRouter.route('/admin/API/images').get(function(req,res){
	console.log(serverPath + req.query['url']);
	var imageName = req.query['url'].split('/');
	imageName = imageName[2];
	console.log(imageName);
	//var readStream = fs.createReadStream('lib/uploads/' + imageName);
	var ws = fs.createWriteStream('uploads/'+ imageName);
	//get file from server and save to directory
	request(serverPath + req.query['url']).pipe(ws).on('close', function(){
		var path = 'uploads/' + imageName;
		fs.readFile(path, function(err,data){
			if (err)
				console.log(error);
			else{
				var fileType = imageName.split('.');
				fileType = fileType[1];
				if(fileType == 'jpeg' || fileType == 'jpg'){
					res.writeHead(200, {'Content-Type': 'image/jpeg'});
					//send the file to the browser
					res.end(data);
				}
				else{
					res.writeHead(200, {'Content-Type': 'image/png'});
                        	        //send the file to the browser
	                                res.end(data);
				}
			}
		});
	});
});










/*********************************************************************************************************************************
** 			API Calls for BI Suite
*********************************************************************************************************************************/


myRouter.route('/admin/API/getRanking').get(function(req,res){
	request(serverPath + 'getRanking', function(error, response, body){
		if(error){
			console.log(error);
			res.send('error');
		}
		else{
			res.send(body);	
		}
	});
});

myRouter.route('/admin/API/getTopEmployees').get(function(req,res){
        request(serverPath + 'getTopEmployees', function(error, response, body){
                if(error){
                        console.log(error);
                        res.send('error');
                }
                else{
                       res.send(body);
                }
        });
});


myRouter.route('/admin/API/getGenerousEmployees').get(function(req,res){
        request(serverPath + 'getGenerousEmployees', function(error, response, body){
                if(error){
                        console.log(error);
                        res.send('error');
                }
                else{
                        res.send(body);
                }
        });
});

myRouter.route('/admin/API/getFrequencyChart').get(function(req,res){
        request(serverPath + 'getFrequencyChart', function(error, response, body){
                if(error){
                        console.log(error);
                        res.send('error');
                }
                else{
                        res.send(body);
                }
        });
});

myRouter.route('/admin/API/getAwardTypes').get(function(req,res){
        request(serverPath + 'getAwardTypes', function(error, response, body){
                if(error){
                        console.log(error);
                        res.send('error');
                }
                else{
                        res.send(body);
                }
        });
});


/************************************************************************************************
Section 4 Calls

************************************************************************************************/



myRouter.route('/admin/API/getRanking/:id').get(function(req,res){
        request(serverPath + 'getRanking/' + req.params.id, function(error, response, body){
                if(error){
                        console.log(error);
                        res.send('error');
                }
                else{
                        res.send(body);
                }
        });
});


//Used for line chart in upper left quadrant
myRouter.route('/admin/API/getPrestigePoints/:id').get(function(req,res){
        request(serverPath + 'getPrestigePoints/' + req.params.id, function(err, response, body){
                if(err){
                        console.log(error);
                        res.send('error');
                }
                else{
                        res.send(body);
                }
        });
});

myRouter.route('/admin/API/getAwardTypes/:id').get(function(req,res){
        request(serverPath + 'getAwardTypes/' + req.params.id, function(err, response, body){
                if(err){
                        console.log(error);
                        res.send('error');
                }
                else{
                        res.send(body);
                }
        });
});

//get awards recieved by user for use in table
myRouter.route('/admin/API/getAwardsRecieved/:id').get(function(req,res){
        request(serverPath + 'getAwardsReceived/' + req.params.id, function(err, response, body){
                if(err){
                        console.log(error);
                        res.send('error');
                }
                else{
                        res.send(body);
                }
        });
});

//get individual awards given to user id for use in table


myRouter.route('/admin/API/userAwards/:id').get(function(req,res){
        request(serverPath + 'userAwards/' +  req.params.id, function(err, response, body){
                if(err){
                        console.log(error);
                        res.send('error');
                }
                else{
                        res.send(body);
                }
        });
});



//Used for Bar Chart for awards given in lower left quadrant

myRouter.route('/admin/API/getAwardsGivenFrequency/:id').get(function(req,res){
        console.log("Getting User Awards Given");
	request(serverPath + 'getAwardsGivenFrequency/' + req.params.id, function(err, response, body){
                if(err){
                        console.log(error);
                        res.send('error');
                }
                else{
                        res.send(body);
                }
        });
});

//Used for PI Chart 

myRouter.route('/admin/API/getAwardTypesGiven/:id').get(function(req,res){
	console.log("Getting Types: " +  req.params.id);
        request(serverPath + 'getAwardTypesGiven/' + req.params.id, function(err, response, body){
                if(err){
                        console.log(error);
                        res.send('error');
                }
                else{
                        res.send(body);
                }
        });
});



myRouter.route('/admin/API/userAwards/:id').get(function(req,res){
        request(serverPath + 'userAwards/' + req.params.id, function(err, response, body){
                if(error){
                        console.log(error);
                        res.send('error');
                }
                else{
                        res.send(body);
                }
        });
});



//Get user ID by Email
myRouter.route('/admin/API/getUserByEmail').post(function(req,res){
	console.log(req.body);
	 request.post(serverPath + 'getUserByEmail', {form: {email: req.body.email}}, function(err, response, body){
                if(err){
                        console.log(err);
                        res.send('error');
                }
                else{
			console.log(body);			
			var result = JSON.parse(body);
			if(result.Data.length == 0){
				res.send({ID: -1});
			}
			else{
				console.log("Sending User ID: " + result.Data[0].userID); 
                	        res.send({
					ID: result.Data[0].userID
				});
                	}
		}
        });
});





/**********************************************************************************************************
**					API LINKS FOR ADMIN
**********************************************************************************************************/


//Handle Remove Create and Update Operations Here. Take data from site and redirect to Database server

myRouter.route('/admin/API/admin').post(
	function(req,res){

		//generate salt value here
		var saltValue = cryptoHash.getRandomSalt();
		var values =  {password: req.body.password, email:  req.body.email, salt:  saltValue };
		
		cryptoHash.hash(saltValue, req.body.password, function(err, passwordHash){
			values.password =  passwordHash;
			console.log(passwordHash);
			request.post({url: serverPath + 'admins', form: values }, function(err, response,body){
		        if(!err && response.statusCode < 400){
                                res.send("Admin Created");
                        }
                        else{
				console.log("ERROR");
                                if(response)
                                        console.log(err);
				res.send("Error Creating User");
                        }
			});		



		});


	});
myRouter.route('/admin/API/admin/:uuID')
	.put(function(req,res){
                var saltValue = cryptoHash.getRandomSalt();
		var values =  {password: req.body.password, email:  req.body.email, salt: saltValue, passwordCode:"0"};


		cryptoHash.hash(saltValue, req.body.password, function(err, passwordHash){		
		        if(req.session.passport.user.id == req.params.uuID){
				values.password = passwordHash;
				request.put({url: serverPath +  'admins/' + req.params.uuID, form:values}, function(err, response,body){
                	        	if(!err && response.statusCode < 400){
	                	                res.send("Admin Updated!");
	        	                }
        	        	        else{
                        		        if(response)
                	                	        console.log(err);
	                        	        console.log(response.body);
        	                        	res.send(err);
 		               	        }
				});
			}
			else{
				console.log("Invalid ID");
				res.send("Invalid Admin ID. A admin can only update there own profile.");
	
			}	
         	});

	})
	.delete(function(req,res){
		console.log("Delete Request for ID: " + req.params.ID);
		request.delete( serverPath + 'admins/' + req.params.uuID, function(err, response,body){
			console.log(req.session);
			if(!err && response.statusCode < 400){
				res.send("Admin Deleted!");
			}
			else{
				console.log("ERRROR!!!!");
				if(response)
					console.log(err);
				console.log(response);
				res.send(err);	
			}
		});
});



/****************************************************************************************************************************************
**							USERS
*****************************************************************************************************************************************/


//Handle Remove Create and Update Operations Here. Take data from site and redirect to Database server

myRouter.route('/admin/API/user')
        //create New Router
        .post(upload.single('avatar'), function(req,res){
		console.log("Body: " + JSON.stringify(req.body));
		//generate salt value here
		var saltValue = cryptoHash.getRandomSalt();
		console.log(req.file);
	
               
		cryptoHash.hash(saltValue, req.body.password, function(err, passwordHash){
		     	var filepath = req.file.path;
			var newFilePath
			if(req.file.mimetype = 'image/jpeg'){
				newFilePath = filepath + '.jpeg';
			}
			else if (req.file.mimetype = 'image/png'){
				newFilePath = filepath + '.png';
			}
			else{
				res.send("Invalid File Type");
				return;
			}
			fs.rename(filepath, newFilePath, function(err){
				if(err) throw err;
				console.log(newFilePath);
        	         	var values =  {
					image: fs.createReadStream(newFilePath), 
					password: req.body.password, 
					email:  req.body.email, 
					salt: saltValue   , 
					region: req.body.region,  
					name: req.body.name, 
					startDate: req.body.startDate
				}; 

				values.password = passwordHash;
				request.post({url: serverPath + '/users', formData: values }, function(err, response,body){
					
                        		if(err){
        	        		        if(response)
                	                	        console.log(err);
	                	   			console.log(response);
					     	        res.send("Error Creating User");

        	        	        }
	        	                else{
	                        	        console.log("User Created!");
	       	                      		res.send({result:"User Created!"});
						fs.unlinkSync(newFilePath);
		                        }
	        	        });
			});
		});
        });

myRouter.route('/admin/API/user/:ID')
        .get(function(req,res){
		console.log("Getting User Data:" + req.params.ID);
		 request.get({url: serverPath + 'users/' + req.params.ID}, function(err, response,body){
                        if(!err && response.statusCode < 400){
                                console.log(body);
                                res.send(body);
                        }
                        else{
                                if(response)
                                        console.log(err);
                                console.log(response.body);
                                res.send(response);
                        }
                });




	})

	.put(upload.single('avatar'),function(req,res){
                //generate salt value here
                var saltValue = cryptoHash.getRandomSalt();

                cryptoHash.hash(saltValue, req.body.password, function(err, passwordHash){
                        var filepath = req.file.path;
                        var newFilePath
                        if(req.file.mimetype = 'image/jpeg'){
                                newFilePath = filepath + '.jpeg';
                        }
			else if(req.file.mimetype = 'image/jpg'){
				newFilePath = filepath + '.jpg';

			}
                        else if (req.file.mimetype = 'image/png'){
                                newFilePath = filepath + '.png';
                        }
                        else{
                                res.send("Invalid File Type");
                                return;
                        }
                        fs.rename(filepath, newFilePath, function(err){
                                if(err) throw err;
                                console.log(newFilePath);
                                var values =  {
                                        image: fs.createReadStream(newFilePath),
                                        passwordCode: req.body.passwordCode,
					password: req.body.password,
                                        email:  req.body.email,
                                        salt: saltValue   ,
                                        region: req.body.region,
                                        name: req.body.name,
                                        startDate: req.body.startDate
                                };

                                values.password = passwordHash;
                     		console.log(values);
			        request.put({url: serverPath + 'users/' + req.params.ID, formData: values }, function(err, response,body){
                                        
					if(err){
                                                if(response)
                                                        console.log(err);
                                                        console.log(response);
                                                        res.send("Error Creating User");

                                        }
                                        else{
                                                console.log("User Updated!");
						console.log(response);
                                                res.send({result:"User Updated!"});
						fs.unlinkSync(newFilePath);
                                        }

                                });
                        });
                });
        })
        .delete(function(req,res){
                console.log("Delete Request for ID: " + req.params.ID);
                request.delete( serverPath + 'users/' + req.params.ID, function(err, response,body){
                        if(!err && response.statusCode < 400){
                                console.log(body);
                                res.send("User Deleted!");
                        }
                        else{
                                if(response)
                                        console.log(err);
                                console.log(response);
                                res.send(err);
                        }
                });



	});







//allow the router to be exported 
module.exports = myRouter;
