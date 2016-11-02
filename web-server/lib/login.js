// Global Variable Decleration
var router = require('express').Router();

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
Desc: Initialises the login routers with authorisation
****************************************/
function init(passport) {
	// Redirect function
	var redirFunc = function(req, res){
		// Handles Admin Logins
		if (req.body.hasOwnProperty('admin-login')) { res.redirect(307, '/login-admin'); }
		// Handles User Logins
		else { res.redirect(307, '/login-user'); }
	}

	// Redirects user and admin logins to correct handler
	router.post('/login', function(req, res, next){
		// Deletes the old session data if it exists
		if (req.session){ req.session.destroy(redirFunc(req, res)); }
		// Else preforms the redirect
		else { redirFunc(req, res) }
	});

	// Handles submitted user logins
	router.post('/login-user', passport.authenticate('user-login', { failureRedirect: '/login' }), function(req, res, next){
		res.redirect('/award/give-award');
	});

	// Handles submitted admin logins
	router.post('/login-admin', passport.authenticate('admin-login', { failureRedirect: '/login' }), function(req, res, next){
		res.redirect('/admin/users');
	});

	// Returns the router
	return router;
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

// Logouts the user
router.get('/logout', function(req, res, next){
	req.session.destroy(function(err){
		res.redirect('/');
	});
});

// Exports the module
module.exports = init;