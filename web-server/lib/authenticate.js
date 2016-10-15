// Requires
localStrategy = require('passport-local').Strategy;

// Dummy users for testing
const user = {
	username: 'test',
	password: 'test',
	id: 1
}

/******************************************
** Var: userLogin
** Desc: Authentication strategy for users
******************************************/
userLogin = function(username, password, done) {
User.findOne({ username: username }, function (err, user) {
		if (err) { return done(err); }
		if (!user) { return done(null, false); }
		if (!user.verifyPassword(password)) { return done(null, false); }
		return done(null, user);
	});
}

// Exports the functions
module.exports = {
	userLogin : userLogin
}