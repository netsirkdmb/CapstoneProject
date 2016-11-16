/*************************************************
** File Name: editName.js
** Author: William McCumstie
** Date: 11/11/2016
** Description: Jquery editting the name
*************************************************/
// Loads code after page has finished loading
$(document).ready(function(){
	// Switches name from "show" to "edit"
	$("#showName").click(function() {
		$(this).hide();
		$("#editName").show();
		$("#editNameInput").val($(this).html());
	})
});