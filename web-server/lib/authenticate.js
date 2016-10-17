// Requires
var passport = require('passport');
var localStrategy = require('passport-local').Strategy;

// Function for serializing the user
passport.serializeUser(function(user, done) {
  done(null, user);
});

// Function for deserializing the user
passport.deserializeUser(function(user, done) {
  done(null, user);
});

// Dummy users for testing
const user = {
	username: 'test',
	password: 'test',
	id: 1
}

/******************************************
** Var: userLogin
** Desc: Authentication strategy for users logins
******************************************/
function userLogin(username, password, done) {
		console.log("This will become a database call");

	if (username != user.username) {return done(null, false);}
	else if (password != user.password) {return done(null, false);}
	else {return done(null, user);}
}

/******************************************
** Var: init
** Desc: Initialises the authentication
******************************************/
function init(app, session) {
	app.use(passport.initialize());
	app.use(passport.session());
	passport.use('user-login', new localStrategy(userLogin));
	return passport;
}

// Exports the functions
module.exports = init;