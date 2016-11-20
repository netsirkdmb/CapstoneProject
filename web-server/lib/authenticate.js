// Requires
var passport = require('passport');
var localStrategy = require('passport-local').Strategy;
var request = require('request');
var hostDB = "http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600";
var async = require('async');
var cryptoHash = require('./cryptoHash.js');

// Function for serializing the user
passport.serializeUser(function(data, done) {
	var user = {}
	user["id"] = data[0];
	user["type"] = data[1];
	done(null, user);
});

// Function for deserializing the user
passport.deserializeUser(function(user, done) {
  done(null, user);
});


/******************************************
** Var: userLogin
** Desc: Authentication strategy for users logins
******************************************/
function userLogin(username, password, done) {
	// Backdoor for testing
	if ((username == 'test') && (password == 'test'))
		return done(null, [1, "award"]);

	// Runs the following commands in series
	async.waterfall([
		// Pulls the data from the database
		function(callback){
			var path = "/getUserByEmail";
			request.post({url:(hostDB + path), form:{"email": username}}, function(err, res, body){
				// An error has occurred
				if (err) callback(true, null);

				// Email not found (or to many response)
				body = JSON.parse(body);
				if (body.Data.length != 1) callback(true, null);

				// Passes the password hash and salt to the next function
				data = body.Data[0];
				callback(false, data.password, data.salt, data.userID);
			});
		},

		// Hashes the password
		function(passwordHashDB, salt, id, callback){
			cryptoHash.hash(salt, password, function(err, passwordHash){
				// An error has occurred
				if (err) callback(true, null);

				// The hash matches
				if (passwordHash == passwordHashDB) callback(false, id);

				// Password hash doesn't match, error
				else { callback(true, null); }
			});
		}

	// Callback function
	], function(err, id){
		// An error has occurred, deny entrance
		if (err) done(null, false);

		// Password matches, allow entrance
		else done(null, [id, "award"]);
	});
}

/******************************************
** Var: adminLogin
** Desc: Authentication strategy for users logins
******************************************/
function adminLogin (username, password, done) {
	// Backdoor for testing
	if ((username == 'test') && (password == 'test'))
		return done(null, [1, "award"]);

	// Runs the following commands in series
	async.waterfall([
		// Pulls the data from the database
		function(callback){
			var path = "/getAdminByEmail";
			request.post({url:(hostDB + path), form:{"email": username}}, function(err, res, body){
				// An error has occurred
				if (err) callback(true, null);

				// Email not found (or to many response)
				body = JSON.parse(body);
				if (body.Data.length != 1) callback(true, null);

				// Passes the password hash and salt to the next function
				data = body.Data[0];
				callback(false, data.password, data.salt, data.adminID);
			});
		},

		// Hashes the password
		function(passwordHashDB, salt, id, callback){
			cryptoHash.hash(salt, password, function(err, passwordHash){
				// An error has occurred
				if (err) callback(true, null);

				// The hash matches
				if (passwordHash == passwordHashDB) callback(false, id);

				// Password hash doesn't match, error
				else callback(true, null);
			});
		}

	// Callback function
	], function(err, result){
		// An error has occurred, deny entrance
		if (err) done(null, false);

		// Password matches, allow entrance
		else done(null, [id, "award"]);
	});
}

/******************************************
** Var: init
** Desc: Initialises the authentication
******************************************/
function init(app, session) {
	app.use(passport.initialize());
	app.use(passport.session());
	passport.use('user-login', new localStrategy(userLogin));
	passport.use('admin-login', new localStrategy(adminLogin));
	return passport;
}

// Exports the functions
module.exports = init;