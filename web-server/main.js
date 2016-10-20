// Loads the https, express, handlebars engine
var express = require('express');
var app = express();
var handlebars = require('express-handlebars').create({defaultLayout:'main'});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.set('port', 3500);

// Sets up the static files
app.use("/public", express.static(__dirname + '/static'));
app.use("/tether", express.static(__dirname + '/node_modules/tether/dist'))

// Sets up the body parser
var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

//Sets up Request Library
var request = require('request');

// Required Modules (Miscellaneous)
var fs = require('fs');

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

// --------- Additional Routers --------
var loginRouter = require('./lib/login.js');
app.use(loginRouter);
var adminRouter = require ('./lib/admin.js');
app.use(adminRouter);

// ------- Automatic GET Router --------
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

// Starts the web page
app.listen(app.get('port'), function(){
  console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});
