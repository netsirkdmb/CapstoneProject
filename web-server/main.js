// Loads the express, handlebars engine
var express = require('express');
var app = express();
var handlebars = require('express-handlebars').create({defaultLayout:'main'});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.set('port', 3500);

// Sets up the static files
app.use("/public", express.static(__dirname + '/static'));
app.use("/bootstrap", express.static(__dirname + '/node_modules/bootstrap/dist'))
app.use("/jquery", express.static(__dirname + '/node_modules/jquery/dist'))
app.use("/tether", express.static(__dirname + '/node_modules/tether/dist'))

// Sets up the body parser
var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Requires additional custom modules
var login = require('./lib/login');

/**************************************
**    START OF WEBSITE HANDLERS      **
**************************************/
// ---------  DEFAULT  -------------
// Redirects to login page
app.get('/',function(req, res, next){
  res.redirect(303, '/login');
});
app.post('/', function(req, res, next){
  res.redirect(303, '/login');
});

// ---------  Additional -----------
// Please consider adding as seperate modules

// Takes the user to the login page
app.get('/login',function(req, res, next){
  res.render('login/main');
});

// Handles Submitted Logins
app.post('/login', function(req, res, next){
  login.mainPostHandler(req, res, next);
});

// Reset Password Page
app.get('/reset-password', function(req, res, next){
  res.render('login/get-reset-code');
});

// Handles reset password attemps
app.post('/login/reset-password', function(req, res, next){
  login.mainResetPassword(req, res, next);
});

// Change password website
app.post('/login/change-password', function(req, res, next){
  res.render('change-password');
});

// ------------

// Error page not found
app.use(function(req, res, next){
  res.status(404);
  res.render('404');
});

// Error server error
app.use(function(err, req, res, next){
  console.error(err.stack);
  res.type('plain/text');
  res.status(500);
  res.render('500');
});

// Starts the web page
app.listen(app.get('port'), function(){
  console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});
