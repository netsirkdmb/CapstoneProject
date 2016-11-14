// Global Variable Decleration
var router = require('express').Router();

/********************************************
** Func: router.route('/*').all
** Desc: Authirisation - Cookie type must match route
** PostCond: Users can't access admin site and vice versa
*********************************************/
router.route('/*').all(function(req, res, next){
	var passport = req.session.passport;
	var path = req.path.split('/');

	// Rejects access if no authentication
	if (passport == undefined)
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