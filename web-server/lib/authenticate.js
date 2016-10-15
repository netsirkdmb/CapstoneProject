// Requires
var passport = require('passport');
var localStrategy = require('passport-local').Strategy;

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
User.findOne({ username: username }, function (err, user) {
		if (err) { return done(err); }
		if (!user) { return done(null, false); }
		if (!user.verifyPassword(password)) { return done(null, false); }
		return done(null, user);
	});
}

/******************************************
** Var: init
** Desc: Initialises the authentication
******************************************/
function init(app, session) {
	app.use(passport.initialize());
	app.use(passport.session());
	passport.use('user-login', userLogin);
	return passport;
}

// Exports the functions
module.exports = init;