// Global Variable Decleration
var router = require('express').Router();
var request = require('request');
var hostDB = "http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600";
var internalError = "An internal error has occured";

// TEMPORARY GLOBAL VARIABLE
var userID = 1;

/*******************************************
** Router: /award/previous-award
** Desc: Displayes all the previous awards given
*******************************************/
router.get('/award/previous-award', function(req, res, next){
	// NEEDS TO BE REPLACED
	console.log("/award/previous-award - USING TEMPORARY userID - NEEDS TO BE FIXED");

	// Pulls previously issued awards for a user
	var path = "/userAwards/" + userID;
	request(hostDB + path, function(err, resDB, body){
		var context = {};
		body = JSON.parse(body);
		// An error has occured
		if (err){
			console.log(err);
			context.errorMssg = internalError;
		}
		// No data found
		else if (body.Data.length == 0)
			context.errorMssg = "No awards found";
		// Data found
		else
			context.data = body.Data
		res.render('award/previous-award', context);
	});
});


/*******************************************
** Router: /award/profile
** Desc: Displayes the profile information
*******************************************/
router.get('/award/profile', function(req, res, next){
	// NEEDS TO BE REPLACED
	console.log("/award/profile - USING TEMPORARY userID - NEEDS TO BE FIXED");

	// Pulls previously issued awards for a user
	var path = "/users/" + userID;
	request(hostDB + path, function(err, resDB, body){
		var context = {};
		body = JSON.parse(body);
		// An error has occured
		if (err){
			console.log(err);
			context.errorMssg = internalError;
		}
		// No data found
		else if (body.Data.length == 0)
			context.errorMssg = "User profile not found";
		// Data found
		else
			context.data = body.Data[0];
		res.render('award/profile', context);
	});
});


// Exports the routers
module.exports = router;