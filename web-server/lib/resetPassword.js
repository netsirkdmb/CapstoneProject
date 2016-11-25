// Required Files
var aws = require("aws-sdk");
var ses = new aws.SES({"region":'us-west-2'});
var router = require("express").Router();
var request = require('request');
var async = require('async');
var crypto = require('crypto');
var hostDB = "http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600";

// Message to be sent
var params = {
  Destination: { /* required */
    ToAddresses: [
      'william.mccumstie@gmail.com'
    ]
  },
  Message: { /* required */
    Body: { /* required */
      Text: {
        Data: 'This is the body', /* required */
        Charset: 'utf-8'
      }
    },
    Subject: { /* required */
      Data: 'This is the Subject', /* required */
      Charset: 'utf-8'
    }
  },
  Source: 'noreply@employeerecognitionangama.co.uk', /* required */
  Tags: [
    {
      Name: 'unknown_key', /* required */
      Value: 'unknown_value' /* required */
    },
    /* more items */
  ]
};
/*
ses.sendEmail(params, function(err, data){
	console.log(ses);
	console.log("err = "+err);
	console.log("data = "+JSON.stringify(data));
});
*/


/*****************************************
** Func: validateEmail()
** Desc: Returns if the email is valid or not
*****************************************/
function validateEmail(mail) {  
	if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))  
    	return (true)   
   	else
    	return (false)  
}  


/*****************************************
** Router: get-reset-code
** Desc: Generates the reset password code
*****************************************/
router.post('/get-reset-code', function(req, res, next){
	// Extracts the data
	var isAdmin = (req.body.admin == "admin");
	var email = req.body.email;
	
	// Validates the email
	if (!validateEmail(email)) {
		res.render('login/get-reset-code', {isInValid: true});
		return;
	}

	// Runs to following commands in series
	async.waterfall([
		// Pulls the current user data
		function(callback){
			var path;
			// Sets the path for db request (user or admin)
			if (!isAdmin)
				path = "/getUserByEmail";
			else
				path = "/getAdminByEmail";

			// Gets the user data
			request.post({url: (hostDB + path), form: {"email": email}}, function(err, resDB, body){
				// An error has occurred
				if (err){
					callback(true, null);
					return;
				}

				// No user data found
				body = JSON.parse(body);
				if ((body.status == "Fail") || (body.Data == undefined) || (body.Data.length != 1))
					callback(true, null);

				// Passes the user data on
				else
					callback(false, body.Data[0]);
			});
		},

		// Generates the reset password code
		function(userData, callback) {
			// TODO: CAN'T UPDATED admin password - no code provided
			if (isAdmin) {
				next("ERROR: No password code returned for admin");
				return;
			}

			// Extracts the ID
			var id;
			if (!isAdmin) {
				id = "u" + userData.userID;
			}

			// Gets the current time stamp (ms from epoch)
			var timeStamp = (new Date).getTime();

			// Randomly generated key
			require('crypto').randomBytes(128, function(err, buffer) {
				// An error has occurred
				if (err) callback(true, null);

				else {
					// Gets the key
					var key = buffer.toString('hex');
					
					// Creates the code and passes the data on
					userData.passwordCode = key + "-" + timeStamp + "-" + id;
					callback(false, userData);		
				}
			});
		}
	
	// Callback - renders the page
	], function(err, result){
		res.render('login/get-reset-code', {sentEmail: true});
	});
});


// Exports the router
module.exports = router;