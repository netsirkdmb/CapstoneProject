/*************************************************
** File Name: deleteAward.js
** Author: William McCumstie
** Date: 11/11/2016
** Description: Jquery for deleting page
*************************************************/
// Loads code after page has finished loading
$(document).ready(function(){
	// Cache for delete form
	var deleteForm;

	// Adds the event listener to all forms
	$("form").each(function(){
		$(this).on("submit", function(e){
			// Stops the form from being submitted
			e.preventDefault();

			// Displays the confirmation and caches the event
			$("#deleteAward").modal("show");
			deleteForm = e.currentTarget;
		});
	});

	// Submits the cached form once confirmed
	$("#confirmDelete").on("click", function(confirm){
		deleteForm.submit();
	});
});