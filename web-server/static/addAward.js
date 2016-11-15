/*************************************************
** File Name: addAward.js
** Author: William McCumstie
** Date: 11/11/2016
** Description: Jquery for adding award
*************************************************/
// Loads code after page has finished loading
$(document).ready(function(){
	// Creates the datetime picker
	$(function () {
        $('#datetimediv').datetimepicker({	
            inline: true,
            sideBySide: true,
            useCurrent: true,
            showTodayButton: true,
            toolbarPlacement: 'bottom'
        });
    });

	// Processes the add award form
	$("#addForm").on("submit", function(e){
		// Stops the form from being submitted by defualt
		e.preventDefault();

		// Closes all currently oppened popovers
		$(".popover").popover('hide');

		// Triggers the popups for incomplete form
		if (!$("#receipientID").val())
			$("#receipientID").popover('show');
		if (!$("#awardTypeID").val())
			$("#awardTypeID").popover('show');

		// Sets the popover background color
    	$(".popover").popover().css("background-color", "red");
		
    	// Exits if not all infomration has been provided
    	if (!$("#receipientID").val() || !$("#awardTypeID").val())
    		return;

    	// Sends the data to the server
    	$.post("add-award",{
    		receipientID: $("#receipientID").val(),
    		awardTypeID: $("#awardTypeID").val(),
    		timedate: $("#datetime").val()
    	})	
	    	// Successfully added	
	    	.done(function(data){
	    		alert("Award added\nThe receipient has been emailed the award")
	    	})

	    	// An error has occured
	    	.fail(function(data){
	    		alert("An error has occured! - Could not issue award");
    		}
    	);
	});
});