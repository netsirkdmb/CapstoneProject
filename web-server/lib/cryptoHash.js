/**************************************
** File: cryptoHash.js
** Date: 11/15/16
** Desc: File for hashing passwords
**************************************/
// Required files
const crypto = require('crypto');
const async = require('async');

// Base cryptographic set-up parameters
var iterations = 10000;
var keyLen = 512;
var digest = "sha512";

// Default error message
var errMssg = [];
errMssg[0] = "Error: An error has occurred";
errMssg[1] = "Correct: hash(salt, password, callback())";
errMssg[2] = "password: Must be a non empty string";
errMssg[3] = "salt: Non-empty string"
errMssg[4] = "func(err, key): [Required] callback function";


/**************************************
** Func: hash()
** Desc: Generates the user specic hash
**************************************/
function hash(salt, password, func){
	// Runs the functions in series
	async.series([
		function(callback){
			// Validates the password
			var valid = true;
			if ((typeof(password) != typeof("")) || (password == "")) valid = false;
			
			// Validates the salt - Included
			if (typeof(salt) != typeof("") || (salt == "")) valid = false;

			// Validates the callback function
			if (typeof(func) != typeof(function(){})) valid = false;
			
			// Returns the result
			if (valid)
				callback(null, "Passed Input Validation");
			else {
				errMssg[0] = "Error: Incorrect input format"
				callback(errMssg, null);
			}
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
		func(err, res[1]);
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