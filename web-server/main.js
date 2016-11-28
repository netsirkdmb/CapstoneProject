/*******************************************
******     START OF MODULE SETUP   *********
*******************************************/
// Required Modules (Miscellaneous)
var fs = require('fs');
var randomString = require('randomstring');

// Loads the express, handlebars engine
var express = require('express');
var app = express();
var handlebars = require('express-handlebars').create({defaultLayout:'main'});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.set('port', 443);

// Sets up the static files
app.use("/public", express.static(__dirname + '/static'));
app.use("/tether", express.static(__dirname + '/node_modules/tether/dist'))

// Sets up express sessions
var session = require('express-session');
app.use(session({
  secret: randomString.generate(),
  resave: false,
  saveUninitialized: false, 
  cookie: { secure: true, maxAge: 60/*min*/*60/*s*/*1000/*ms*/}
}));

// Sets up the https server
var https = require('https');
var privateKey = fs.readFileSync('../../../.https/domain.key', 'utf8');
var certificate = fs.readFileSync('../../../.https/cert.key', 'utf8');
var credentials = {key: privateKey, cert: certificate};

// Loads the authentication module
var passport = require('./lib/authenticate')(app, session);

// Sets up the body parser
var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false, limit:'50mb' }));
app.use(bodyParser.json({limit:'50mb'}));

// Allows self signed cert for requests
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0"

// ------ END MODULE SETUP -----------
/**************************************
**    START OF WEBSITE HANDLERS      **
**************************************/
// Loads the authorization module
app.use(require('./lib/authorization.js'));

// URI Clean-up: Removes trailing slash
app.use(function(req, res, next) {
   if(req.url.substr(-1) == '/' && req.url.length > 1)
       res.redirect(301, req.url.slice(0, -1));
   else
       next();
});

// -------- Authenticated Routers -------
app.use(require('./lib/base.js')); // Routers: '/'
app.use(require('./lib/login.js')(passport)); // Login + Logout
app.use(require('./lib/resetPassword.js')); // Reset password routers
var adminRouter = require('./lib/admin.js');
app.use(adminRouter);
var awardRouter = require('./lib/award.js');
app.use(awardRouter);

// ------- Prevents Auto-Routing -------
app.get('/layouts*', function(req, res, next){
  res.status(404);
  res.render('404');
});
app.get('/partials*', function(req, res, next){
  res.status(404);
  res.render('404');
});

// ------- Catch-All GET Router --------
app.get('/*', function(req, res, next) {
  // Gets the file name of the handlebars template
  var url = req.originalUrl;
  if (url[url.length - 1] == '/') // Removes trialing '/'
    url = url.substring(0, url.length - 1); 
  var filename = "views" + url + ".handlebars";  

  // Checks if the file exists
  fs.stat(filename, function(err, stats){
    // Skips the handler if no file was found
    if (err)
      next();
    // Renders the page
    else
      res.render(url.substring(1));
  });
});

// ------------ Error ---------------
// Error page not found
app.use(function(req, res, next){
  res.status(404);
  res.render('404');
});

// Error server error
app.use(function(err, req, res, next){
  console.error(err);
  res.status(500).render('500');
});
/*********** END HANDLERS ***********/

/*********************************************
***  LAUNCHES THE HTTP AND HTTPS SERVERS   ***
*********************************************/
// Starts the web page (HTTPS)
var httpsServer = https.createServer(credentials, app);
httpsServer.listen(app.get('port'), function(){
  console.log('Express started on https://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});

// Creates the http redirect server
var appRedir = express();
appRedir.set('port', 80);
appRedir.use(function(req, res, next){
  if (!req.secure)
    res.status(301).redirect('https://' + req.hostname);
  else
    next();
});

// Handles errors on the HTTP server
appRedir.use(function(err, req, res, next){
  console.log(err);
  res.status(400).send();
});

// Starts the web page (HTTP)
appRedir.listen(appRedir.get('port'), function(){
  console.log('Express started on http://localhost:' + appRedir.get('port') + '; press Ctrl-C to terminate.');
});
