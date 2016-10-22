// Required Modules (Miscellaneous)
var fs = require('fs');
var randomString = require('randomstring');

// Loads the express, handlebars engine
var express = require('express');
var app = express();
var handlebars = require('express-handlebars').create({defaultLayout:'main'});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.set('port', 3500);

// Sets up express sessions
var session = require('express-session');
app.use(session({
  secret: randomString.generate(),
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false, maxAge: 10*60*1000}
}));

// Sets up the https server
var https = require('https');
var privateKey = fs.readFileSync('keys/key.pem', 'utf8');
var certificate = fs.readFileSync('keys/cert.pem', 'utf8');
var credentials = {key: privateKey, cert: certificate};

// Loads the authentication module
var passport = require('./lib/authenticate')(app, session);

// Sets up the static files
app.use("/public", express.static(__dirname + '/static'));
//app.use("/bootstrap", express.static(__dirname + '/node_modules/bootstrap/dist'))
//app.use("/jquery", express.static(__dirname + '/node_modules/jquery/dist'))
app.use("/tether", express.static(__dirname + '/node_modules/tether/dist'))

// Sets up the body parser
var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Removes trailing forward slash
app.use(function(req, res, next) {
   if(req.url.substr(-1) == '/' && req.url.length > 1)
       res.redirect(301, req.url.slice(0, -1));
   else
       next();
});

/**************************************
**    START OF WEBSITE HANDLERS      **
**************************************/
// ---------  Default  -------------
// Redirects to login page
app.get('/',function(req, res, next){
  res.redirect(303, '/login');
});
app.post('/', function(req, res, next){
  res.redirect(303, '/login');
});

// ------------ AUTHENTICATE -------------
// Authenticates login post
//next() --> additional routers

// --------- Additional Routers --------
var loginRouter = require('./lib/login.js');
loginRouter.init(passport);
app.use(loginRouter.router);
var adminRouter = require('./lib/admin.js');
app.use(adminRouter);
var userRouter = require('./lib/user.js');
app.use(userRouter.router);

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
  console.error(err.stack);
  res.type('plain/text');
  res.status(500);
  res.render('500');
});
/*********** END HANDLERS ***********/

// Starts the web page (On https)
var httpsServer = https.createServer(credentials, app);
httpsServer.listen(app.get('port'), function(){
  console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});
