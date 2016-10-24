/******************************************************************************************************************************************
** File Name: admins.js
** Author: Bryant Hall
** Date: 10/23/2016
** Description: Jquery and javascript for users js page. Handles basic create, update and delete requests back to web server.
******************************************************************************************************************************************/

//Load code into document when document is done loading
$(document).ready(function(){
	//code block to showing row data in modal
	$("#admintable tr").click(function(){
        	var modalData = [];
		
		$(this).find("td").each(function(){
	            modalData.push($(this).html());
        	});
		console.log(modalData);
		$('#uuID').text(modalData[0]);
		$('#editadminname').val(modalData[1]);
		$('#editadminemail').val(modalData[2]);
		$('#editadminpwd').val(modalData[3]);
		$('#updateUser').modal('show');
		
	});

	//code block to show modal for new admin button
	$('#newadminbutton').click(function(){


		$('#newAdminModal').modal('show');
	});
	
	//Create new Admin Button
	$('#createadminbutton').click(function(){
		//check user has filled out the form
		if($('#name').val()=="" || $('#pwd').val()=="" || $('#email').val() == ""){
			if( $('#name').val() =="")
				alert('Please Fill out Username');
			else if ($('#pwd').val() == "")
				alert('Please Fill out Password.');
			else
				alert('Please Fill out Email');		
			return;
		}

		var formData  = "password=" + $('#pwd').val() + "&uuID=" + $('#name').val() + "&email="+ $('#email').val();
		$.ajax({
			url: '/adminAPI/admin',
			contentType: 'application/x-www-form-urlencoded',
			type: "POST",
			data: formData
		})

		.done(function(result){
			console.log(result);
			if(result.Status == 400) {
				alert('Bad Request');
			}
			else{
				alert(JSON.stringify(result));
				location.reload();
			}
		})
		.fail(function(result){
			alert("Fail");
		})
		;
	});


	//Delete Admin Button
	$('#deleteadminbutton').click(function(){
		var userID = $('#uuID').text();
		$.ajax({
			url: '/adminAPI/admin/' + userID,
			type:"DELETE"
		})
		.done(function(result){
			if(result == "1"){
				alert('User ' + userID + ' Deleted!');
				location.reload();			
			}
			else
				alert("Delete Failed");	
		
		})
		.fail(function(result){
			alert('Failed: ' + result);
		});


	});

	$('#updateadminbutton').click(function(){
		//add code to check form values are filled out
		if( $('#editadminname').val()=="" || $('#editadminpwd').val()=="" || $('#editadminemail').val()==""){
			if($('#editadminname').val()==""){
				alert('Please Fill Out Admin Name.');
			}
			else if( $('#editadminpwd').val()==""){
				alert('Please Fill Out Admin Password.');
			}
			else{
				alert('Please Fill Out Admin Email.');
			}

			return;
		}
		var userID = $('#uuID').text();
		var formData = {
			uuid:$('#editadminname').val()   ,
			email: $('#editadminpwd').val()  ,
			password:  $('#editadminemail').val()

		};
		$.ajax({
			url: '/adminAPI/admin/' + userID,
			data: formData,
                        type:"PUT"

		})
		.done(function(result){
			alert(result);
		})
	
		.fail(function(result){
			alert(failed);
		});
	});
});
