// Required Files
var router = require("express").Router();
var request = require('request');
var async = require('async');
var crypto = require('crypto');
var hostDB = "http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600";
var fs = require('fs');
var aws = require("aws-sdk");
var ses = new aws.SES({"region":'us-west-2'});
var epoch = 1480052740669;

// Message to be sent
var Email = {
	// Email object
	params: {
	  Destination: { /* required */
	    ToAddresses: []
	  },
	  Message: { /* required */
	    Body: { /* required */
	      Text: {
	        Data: "", /* required */
	        Charset: 'utf-8'
	      }
	    },
	    Subject: { /* required */
	      Data: 'Reset Password', /* required */
	      Charset: 'utf-8'
	    }
	  },
	  Source: 'noreply@employeerecognitionangama.co.uk'
	},

	body: function(name, passwordCode) {
		var body = "Dear " + name + ',\n\n';
		body += "Please follow the link provided in order to reset your password. "
		body += "The password code provided will be valid for up to 24hrs.\n\n"
		body += "Link: https://www.employeerecognitionangama.co.uk/login/change-password\n";
		body += "Password Code: " + passwordCode + "\n\n";
		body += "Regards,\n";
		body += "Employee Recognition Team\n";
		return body;
	},

	// Sends the message
	sendEmail: function(email, name, passwordCode, callback) {
		this.params.Destination.ToAddresses.push(email);
		this.params.Message.Body.Text.Data = this.body(name, passwordCode);
		ses.sendEmail(this.params, callback);
	}
}

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
router.post('/login/get-reset-code', function(req, res, next){
	// Extracts the data
	var isAdmin = (req.body.admin == "admin");
	var email = req.body.email;
	
	// Validates the email
	if (!validateEmail(email)) {
		res.render('login/get-reset-code', {isInValid: true});
		return;
	}

	// Sets the path for db request (user or admin)
	var path;
	if (!isAdmin)
		path = "/getUserByEmail";
	else
		path = "/getAdminByEmail";

	// Runs to following commands in series
	async.waterfall([
		// Pulls the current user data
		function(callback){
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
			// Extracts the ID
			var id, codeID;
			if (!isAdmin) {
				id = userData.userID;
				codeID = "u" + id;
			}
			else {
				id = userData.adminID;
				codeID = "a" + id;
			}

			// Gets the current time stamp (ms from epoch)
			var timeStamp = (new Date).getTime() - epoch;

			// Randomly generated key
			require('crypto').randomBytes(32, function(err, buffer) {
				// An error has occurred
				if (err) callback(true, null);

				else {
					// Gets the key
					var key = buffer.toString('hex');
					
					// Creates the code and passes the data on
					userData.passwordCode = key + "-" + timeStamp + "-" + codeID;
					callback(false, userData, id);		
				}
			});
		},

		// Updates the database with the new password code
		function(userData, id, callback) {
			// Makes the request
			request.put({url: hostDB + path, form: userData}, function(err, resDB){
				body = JSON.parse(resDB.body);
				// An error
				if (err) callback(true, null);

				// Rejects failed adds
				if (body.Status != "Success") callback(true, null);

				// Pass user data to the next function
				else callback(null, userData);
			});
		},

		// Emails the code out
		function(userData, callback){
			// Updates admin names
			if (isAdmin)
				userData.name = userData.email;

			// Emails the code
			Email.sendEmail(userData.email, userData.name, userData.passwordCode, function(err, data){
				callback(null, null);
			});
		}
	
	// Callback - renders the page
	], function(err, result){
		res.render('login/get-reset-code', {sentEmail: true});
	});
});


/*****************************************
** Router: reset-password
** Desc: Processes the reset password form
*****************************************/
router.post('/login/change-password', function(req, res, next){
	// Extracts the data
	var code = req.body.code;
	var pass1 = req.body.newpass1;
	var pass2 = req.body.newpass2;
	var isAdmin = null;
	var id;
	var pathEmail, pathID;

	// Runs the following in series
	async.waterfall([
		// Validates the inputs and confirms the code matches
		function(callback){
			// Confirms data was extracted properly
			if ((code == undefined) || (pass1 == undefined) || (pass2 == undefined)) {
				callback(true, null);
				return;
			}

			// Confirms the code is in the correct format
			var regexCode = /\w+-[0-9]+-(a|u)[0-9]+\0/;
			if (!regexCode.test(code + '\0')) {
				callback(true, null);
				return;
			}

			// Confirms the password match and type
			if (pass1 != pass2) {
				callback(true, null);
				return;
			}
			var regexPass = /\w+/;
			if (!regexPass.test(pass1)){
				callback(true, null);
				return;
			}

			// Extracts the user type from the code
			var regexAdmin = /-a[0-9]+/;
			var regexUser = /-u[0-9]+/;
			if (regexAdmin.test(code)) isAdmin = true;
			else isAdmin = false;

			// Extracts the id and sets the path variables
			if (isAdmin) {
				id = regexAdmin.exec(code)[0].slice(2);
				pathEmail = "/getAdminByEmail";
				pathID = "/admins/" + id;
			}
			else {
				id = regexUser.exec(code)[0].slice(2);
				pathEmail = "/getUserByEmail";
				pathID = "/users/" + id;
			}

			// Confirms the code matches the one in the database
			request.get(hostDB + pathID, function(err, resDB){
				// Converts the body to JSON
				if (resDB.body != undefined)
					var body = JSON.parse(resDB.body);
				else {
					callback(true, null);
					return;
				}
			
				// An error has occurred
				if (err) callback(true, null);

				// Confirms the status
				else if (body.Status != "Success")
					callback(true, null);

				// Confirms the co
			});
		}

	// Callback function
	], function(err, result){
		// An error occurred, password not reset
		if (err) res.render('login/change-password', {failed: true});

		// Else added correctly
		else res.render('login/change-password', {success: true});
	})
});


// Exports the router
module.exports = router;