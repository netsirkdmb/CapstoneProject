// Global Variable Deceleration
var router = require('express').Router();

/********************************************
** Func: router.route('/*').all
** Desc: Authorization - Cookie type must match route
** PostCond: Users can't access admin site and vice versa
*********************************************/
router.route('/*').all(function(req, res, next){
	var passport = req.session.passport;
	var path = req.path.split('/');

	// Allows access to login pages
	if (path[1] == 'login')
		next();

	// Rejects access if no authentication
	else if (passport == undefined)
		res.redirect('/login');

	// Allows access if type matches
	else if (path[1] == passport.user.type)
		next();

	// Denies entry
	else
		res.redirect('/login');
});

// Exports the router
module.exports = router;