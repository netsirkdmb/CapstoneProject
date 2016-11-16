/**************************************
** File: cryptoHash.js
** Date: 11/15/16
** Desc: File for hashing passwords
**************************************/
// Required files
const crypto = require('crypto');
const async = require('async');
const request = require('request');

// Database address
var hostDB = "http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600";

// Base cryptographic set-up parameters
var iterations = 10000;
var keyLen = 512;
var digest = "sha512";
var secret;
var saltGlobal = "NEED TO ADD THE SALT";

// Default error message
var errMssg = [];
errMssg[0] = "Error: An error has occured";
errMssg[1] = "Correct: hash(userID, password, callback()) [, salt]";
errMssg[2] = "userID: Must be greater than 0";
errMssg[3] = "password: Must be a non empty string";
errMssg[4] = "salt: [OPTIONAL] Non-empty string"
errMssg[5] = "func(err, key): [Required] callback function";


/**************************************
** Func: hash()
** Desc: Generates the user specic hash
**************************************/
function hash(userID, password, func, salt){
	// Runs the functions in series
	async.series([
		function(callback){
			// Validates the userID and password
			var valid = true;
			if ((typeof(userID) != typeof(0)) || (userID < 1)) valid = false;
			if ((typeof(password) != typeof("")) || (password == "")) valid = false;
			
			// Validates the salt - Included
			if (typeof(salt) == typeof("")) {
				if ((typeof(salt) != typeof("")) || (salt == ""))
					valid = false;
			}

			// Checks for invalid salt type
			else if (salt != undefined)
				valid = false;

			// Validates the callback function
			if (typeof(func) != typeof(function(){}))
				valid = false;
			
			// Returns the result
			if (valid)
				callback(null, "Passed Input Validation");
			else {
				errMssg[0] = "Error: Incorrect input format"
				callback(errMssg, null);
			}
		},
		
		// Gets the salt from the (if required) 
		function(callback) {
			if (salt == undefined) {
				var path = "/users/" + userID;
				request(hostDB + path, function(err, res, body) {
					// An erorr has occured
					if (err) {
						callback(err, 0); 
						return;
					}

					// Could not find user account
					data = JSON.parse(body).Data;
					if (data.length == 0) {
						errMssg[0] = "Error: Could not find user";
						callback(errMssg, false);
					}

					// Updates the salt
					else {
						salt = saltGlobal;
						callback(false, salt);
					}
				});
			}

			// Returns the inputted salt
			else
				callback(false, salt);
		},

		// Hashes the password and salt
		function(callback){
			// Hashes the password
			crypto.pbkdf2(password, salt, iterations, keyLen, function(err, key) {
				// An error has occured
				if (err) { 
					callback(err, 0);
				}

				// Passes the key to the callback
				else 
					callback(false, key.toString('hex'));
			});
		}

	// Runs there call back function
	], function(err, res){
		func(err, res[2]);
	});
}


/**************************************
** Func: getRandomSalt()
** Desc: Generates a random salt
**************************************/
function getRandomSalt() {
	return crypto.randomBytes(16).toString('hex');
}

// Exports the module
module.exports = {
	hash : hash,
	getRandomSalt : getRandomSalt
}

salt = getRandomSalt();
console.log(salt);
hash(1, "wm", function(err, key){console.log(key)}, salt);