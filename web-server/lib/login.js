// Global Variable Decleration
var router = require('express').Router();
var routerAuth = require('express').Router();

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
		console.log(req);
		res.redirect('/award/give-award');
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
Func: Init
Desc: Initialises the router with authentication
****************************************/
function init(passport) {
	// Handles Submitted Logins
	router.post('/login', passport.authenticate('user-login'), function(req, res, next){
		mainPostHandler(req, res, next);
	});
};

/****************************************
************ Login Routers **************
****************************************/
// Main login page
router.get('/login',function(req, res, next){
  res.render('login');
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

// Exports the module
module.exports = {
	init : init,
	router : router
}