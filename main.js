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
app.use("/jquery", express.static(__dirname + '/node_modules/bootstrap/node_modules/jquery/dist'))
app.use("/tether", express.static(__dirname + '/node_modules/bootstrap/node_modules/tether/dist'))


// Sets up the body parser
var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Takes user to the add data page
app.get('/',function(req,res){
  //res.render('add-data');
});

// Redirects user to add data after submitting the form
app.post('/', function(req, res){
	// NOTHING HERE
});

// Error page not found
app.use(function(req,res){
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
