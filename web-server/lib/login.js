// Global Variable Decleration

/****************************************
Func: mainPostHandler
Desc: Handles the submitted login form from '/'
****************************************/
function mainPostHandler(req, res, next) {
	// Handles Admin Logins
	if (req.body.hasOwnProperty('admin-login')) {
		res.redirect('/admin/dummyFile');

	// Handles User Logins
	} else {
		res.redirect('/award');
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
Func: runHandlers
Desc: Handles get and post requests
****************************************/
function runHandlers(app) {
	// Takes the user to the login page
	app.get('/login',function(req, res, next){
	  res.render('login');
	});

	// Handles Submitted Logins
	app.post('/login', function(req, res, next){
	  login.mainPostHandler(req, res, next);
	});

	// Reset Password Page
	app.get('/login/reset-password', function(req, res, next){
	  res.render('login/get-reset-code');
	});

	// Handles reset password attemps
	app.post('/login/reset-password', function(req, res, next){
	  login.mainResetPassword(req, res, next);
	});

	// Change password website
	app.post('/login/change-password', function(req, res, next){
	  res.render('login/change-password');
	});
}

/****************************************
EXPORTS: Exports the function listed below
****************************************/
module.exports = {
	runHandlers : runHandlers,
	mainPostHandler : mainPostHandler,
	mainResetPassword : mainResetPassword,
};