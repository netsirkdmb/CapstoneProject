// Global Variable Decleration

/****************************************
Func: mainPostHandler
Desc: Handles the submitted login form from '/'
****************************************/
function mainPostHandler(req, res, next) {
	// Handles Admin Logins
	if (req.body.hasOwnProperty('admin-login')) {
		res.redirect('/dummy-admin-page-404');

	// Handles User Logins
	} else {
		res.redirect('/give-certificate');
	}
}

/****************************************
Func: mainResetPassword
Desc: Handles submitted forms for password resets
****************************************/
function mainResetPassword(req, res, next) {
	// Handles the reset (code provided)
	if (req.body.hasOwnProperty('code')) {
		res.redirect('/change-password');
	
	// Generates a code for the user
	} else {
		res.render('login');
	}
}

/****************************************
EXPORTS: Exports the function listed below
****************************************/
module.exports = {
	mainPostHandler : mainPostHandler,
	mainResetPassword : mainResetPassword,
};