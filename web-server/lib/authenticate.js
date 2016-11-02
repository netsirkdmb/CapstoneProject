// Requires
var passport = require('passport');
var localStrategy = require('passport-local').Strategy;
var request = require('request');
var hostDB = "http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600";

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

	// Pulls the password saved in the database
	var path = "/getUserByEmail";
	request.post({url:(hostDB + path), form:{"email": username}}, function(err, res, body){
		body = JSON.parse(body);
		// Prevents access if there is an error
		if (err)
			return done(err); 
		// Email not found (or to many response)
		else if (body.Data.length != 1)
			return done(null, false);
		// Correct password supplied
		else if (body.Data[0].password == password)
			return done(null, [body.Data[0].userID, "award"]);
		// Catch all - denied access
		else
			return done(null, false);
	});
}

/******************************************
** Var: adminLogin
** Desc: Authentication strategy for users logins
******************************************/
function adminLogin (username, password, done) {
	// Backdoor for testing
	if ((username == 'test') && (password == 'test'))
		return done(null, [1, "admin"]);

	// Pulls the password saved in the database
	var path = "/getAdminByEmail";
	request.post({url:(hostDB + path), form:{"email": username}}, function(err, res, body){
		body = JSON.parse(body);
		// Prevents access if there is an error
		if (err)
			return done(err); 
		// Email not found (or to many response)
		else if (body.Data.length != 1)
			return done(null, false);
		// Correct password supplied
		else if (body.Data[0].password == password)
			return done(null, [body.Data[0].adminID, "admin"]);
		// Catch all - denied access
		else
			return done(null, false);
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