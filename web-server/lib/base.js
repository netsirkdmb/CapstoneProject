// Global Variable Deceleration
var router = require('express').Router();

// Redirects to login page
router.get('/',function(req, res, next){
  res.redirect(303, '/login');
});
router.post('/', function(req, res, next){
  res.redirect(303, '/login');
});

// Exports the router
module.exports = router;