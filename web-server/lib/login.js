// Global Variable Decleration
var express = require('express');
var router = express.Router();
var passport;

/****************************************
Func: mainPostHandler
Desc: Handles the submitted login form from '/'
****************************************/
function mainPostHandler(req, res, next) {
	// Records the user as logged in
	// NOTE: Do not use for security purposes - only forces the save
	req.session.login = true; // Do not use

	// Handles Admin Logins
	if (req.body.hasOwnProperty('admin-login')) {
		res.redirect('/admin/dummy');

	// Handles User Logins
	} else {
		res.redirect('/award/dummy');
	}
}

/****************************************
Func: mainResetPassword
Desc: Handles submitted forms for password resets
****************************************/
function mainResetPassword(req, res, next) {
	// Handles the reset (code provided)
	if (req.body.hasOwnProperty('code')) {
		res.redirect(307, '/login/change-password');
	
	// Generates a code for the user
	} else {
		res.redirect('/login/reset-password');
	}
}

/****************************************
************ Login Routers **************
****************************************/
router.get('/login',function(req, res, next){
  res.render('login');
});

// Handles Submitted Logins
router.post('/login', function(req, res, next){
  mainPostHandler(req, res, next);
});

// Reset Password Page
router.get('/login/reset-password', function(req, res, next){
  res.render('login/get-reset-code');
});

// Handles reset password attemps
router.post('/login/reset-password', function(req, res, next){
  mainResetPassword(req, res, next);
});

// Change password website
router.post('/login/change-password', function(req, res, next){
  res.render('login/change-password');
});


/****************************************
Func: module.export
Desc: Initialises the router (inc authentication)
****************************************/
module.exports = function(pass){
	passport = pass;

	// returns the router
	return router;
}
