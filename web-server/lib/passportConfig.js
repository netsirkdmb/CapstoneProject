// Global variables
var passport;

/**********************************
** Func: Init
** Desc: Initialises the 
**********************************/
function init(pass) {
	passport = pass;
}


// Exports the module
module.exports = {
	init : init
}