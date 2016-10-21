//Code block for admins page. Add click functionality for items on a table and a new button
$(document).ready(function(){
	//code block to showing row data in modal
	$("#admintable tr").click(function(){
        	var modalData = [];
		
		$(this).find("td").each(function(){
	            modalData.push($(this).html());
        	});
		console.log(modalData);
		$('#editadminname').val(modalData[0]);
		$('#editadminemail').val(modalData[1]);
		$('#editadminpwd').val(modalData[2]);
		$('#updateUser').modal('show');
		
	});

	//code block to show modal for new admin button
	$('#newadminbutton').click(function(){
		$('#newAdminModal').modal('show');
	});
});
