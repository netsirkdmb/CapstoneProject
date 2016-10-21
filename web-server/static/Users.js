//Jquery for table data and add new user button

$(document).ready(function(){
    $("#userstable tr").click(function(){
        var modalData = [];
		
		$(this).find("td").each(function(){
            
			
				modalData.push($(this).html());
			
			//alert($(this).html());
        });
		console.log(modalData);
		$('#editname').val(modalData[0]);
		$('#editemail').val(modalData[1]);
		$('#editpwd').val(modalData[2]);
		$('#editimage').val(modalData[4]);
		$('#editregion').val(modalData[5]);
		
		$('#editusers').modal('show');
		
    });
	
	$('#newuserbutton1').click(function(){
		//alert('test');
		$('#createusermodal').modal('show');
	});
});
