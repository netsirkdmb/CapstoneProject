// Global Variable Decleration
var router = require('express').Router();
var request = require('request');
var async = require('async');
var internalError = "An internal error has occured";
var hostDB = "http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600";

/*******************************************
** Func: dateSortFunc
** Desc: Function for sorting awards into date order
** PreCond: The time and date must be extracted
** Return: The data order of the two objects passed in
*******************************************/
function dateSortFunc(a, b){
	// Extracts the date data YYYY, MM, DD, HH, MM, SS, mSmS
	var date1 = a.awardDate.split(/ |-|:|,/);
	var date2 = b.awardDate.split(/ |-|:|,/);

	// Compares the dates
	for (c = 0; c < date1.length; c++){
		if (date1[c] != date2[c])
			return date1[c] - date2[c];
	}

	// Else returns they are the same
	return 0;
}


/*******************************************
** Func: emailSortFunc
** Desc: Function for sorting users by email
** PreCond: Object must contain email field
** Return: The email order of the objects
*******************************************/
function emailSortFunc(a, b){
	// Extracts the emails
	var e1 = a.email.split('@');
	var e2 = b.email.split('@');

	// Sorts the emails by domain first
	if (e1[1] != e2[1]) 
		return (e1[1] > e2[1] ? 1 : -1);

	// Then sorts by email name
	else if (e1[0] != e2[0])
		return (e1[0] > e2[0] ? 1 : -1);

	// Returns they match -- should be imposible
	else
		return 0;
}


/*******************************************
** Func: awardSortFunc
** Desc: Function for sorting award types by name
** PreCond: Object must contain name feild
** Return: The award order of the objects
*******************************************/
function awardSortFunc(a, b){
	// Match
	if (a.name == b.name)
		return 0;
	// Non-match
	else
		return (a.name > b.name ? 1 : -1);
}


/*******************************************
** Router: /award
** Desc: Redirects to /award/previous-award
*******************************************/
router.get('/award', function(req, res, next){
	res.redirect('/award/give-award');
});

/*******************************************
** Router: /award/previous-award
** Desc: Displayes all the previous awards given
*******************************************/
router.get('/award/previous-award', function(req, res, next){
	// Pulls the user ID from the session
	var userID = req.session.passport.user.id;

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
		
		// Processes the data found
		else {
			// Spilts the time date object
			var data = body.Data;
			var dateArr;
			for (c = 0; c < data.length; c++){
				dateArr = data[c].awardDate.split(/ |,|-|:/);
				data[c].date = "" + dateArr[1] + "-" + dateArr[2] + "-" + dateArr[0];
				data[c].time = "" + dateArr[3] + ":" + dateArr[4];
			}

			// Sorts the data into date order
			data.sort(dateSortFunc);

			// Saves the data in the context
			context.data = data;
		}

		// Displays the page
		res.render('award/previous-award', context);	
	});
});


/*******************************************
** Router: /award/give-award
** Desc: Populates the form with the database data and displays the page
*******************************************/
router.get('/award/give-award', function(req, res, next){
	// Runs the following db queries in parallel
	async.parallel({
		// Gets the user list from the database
		userList: function(callback){
			var path = '/users';
			request(hostDB + path, function(err, resDB, body){
				// An error has occured
				if (err)
					callback(err, null);

				// Sorts and saves the body data to the context
				else 
					callback(null, JSON.parse(body).Data.sort(emailSortFunc));
			});
		},

		// Gets the award type list
		awardList: function(callback){
			var path = '/awardTypes';
			request(hostDB + path, function(err, resDB, body){
				// An error has occured
				if (err)
					callback(err, null);

				// Sorts and saves the body data to the context
				else 
					callback(null, JSON.parse(body).Data.sort(awardSortFunc));
			});
		}

	// Callback function - Runs at the end context contains the results
	}, function(err, context){
		// An error has occured
		if (err)
			next(err);

		// Renders the pages
		else
			res.render('award/give-award', context);
	});
});


/*******************************************
** Router: /award/profile
** Desc: Displayes the profile information
*******************************************/
router.get('/award/profile', function(req, res, next){
	// Pulls the user ID from the session
	var userID = req.session.passport.user.id;

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
		
		// Renders the page
		res.render('award/profile', context);
	});
});


/*******************************************
** Router: /award/deleteAward
** Desc: Deletes the award
*******************************************/
router.post('/award/deleteAward', function(req, res, next){
	// Runs the function in series
	async.waterfall([
		// Gets the award ID from the form
		function(callback){
			// Error - no ID provided
			if (req.body.id == null)
				callback(true, null);

			// Passes the id to the next function
			else
				callback(null, req.body.id);
		},

		// Checks the user owns the award
		function(awardID, callback){
			// Queries the database for the award details
			var path = "/awards/" + awardID;
			request(hostDB + path, function(err, resDB, body){
				// An error has occured
				if (err)
					callback(true, null);

				// Confirms the user created the award
				else {
					var loggedInUser = req.session.passport.user.id;
					var awardUser = JSON.parse(body).Data[0].giverID;
						
					// Match - Deletes the entry
					if (loggedInUser == awardUser)
						callback(null, path);

					// Doesn't match - SKIPS delete
					else
						callback(true, null);
				}
			});
		},

		// Deletes the award
		function(path, callback){
			// Deletes the award
			request.delete(hostDB + path, function(){
				callback(null);
			});
		}

	// Callback function - redirects to previous-award
	], function(err, result){
		res.redirect('previous-award');
	});
});


/*******************************************
** Router: /award/add-award
** Desc: processes form data to add award
*******************************************/
router.post('/award/add-award', function(req, res, next){
	// Extracts the data
	var receiverID = parseInt(req.body.receipientID, 10);
	var awardTypeID = parseInt(req.body.awardTypeID, 10);
	var bodyTime = req.body.timedate;

	// Confirms the ID's are numbers
	if (!receiverID || !awardTypeID){
		res.status(400).send(null);
		return;
	}

	// Confirms the data follows the correct patern
	
});

// Exports the routers
module.exports = router;