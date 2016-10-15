// Global Variable Decleration
var express = require('express'); 
var myRouter = express.Router(); 
/*****************************************************
		Login Routers 
*****************************************************/ 

//renders users page with dummy data 
myRouter.get('/users' , function (req,res){
	//get data from server here in future
	var context = {};
	
	context.data = [
	{ name:"bryant", email:"bbbg19@gmail.com", password:"123", time:"8:00am", image:"", region:"Northwest"},
	{ name:"bryant1", email:"bbbg14@gmail.com", password:"1234", time:"8:00am", image:"", region:"Northwest"},
	{ name:"bryant2", email:"bbbg13@gmail.com", password:"12345", time:"8:00am", image:"", region:"westnorth"},
	{ name:"bryant3", email:"bbbg192@gmail.com", password:"123456", time:"8:00am", image:"", region:"Eastwest"},
	{ name:"bryant4", email:"bbbg191@gmail.com", password:"12", time:"8:00am", image:"", region:"Soutwest"}
	];
	
	res.render('admin/users', context);
});

//renders admin page with dummy data 
myRouter.get('/admins', function(req,res){
	//get data from server here
	var context = {};
	context.data = [
		{name:"bob", email:"yomommasofat", password:"1", time: "8:00am"},
		{name:"bob1", email:"yomommasofat1", password:"12", time: "8:01am"},
		{name:"bob2", email:"yomommasofat2", password:"123", time: "8:02am"}
	];
	res.render('admin/admins', context);
});

//renders business intelligence page 
myRouter.get('/bi', function(req,res){
	res.render('admin/bi');
});

//allow the router to be exported 
module.exports = myRouter;
