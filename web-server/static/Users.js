/******************************************************************************************************************************************
** File Name: Users.js
** Author: Bryant Hall
** Date: 10/23/2016
** Description: Jquery and javascript for users js page. Handles basic create, update and delete requests back to web server.
******************************************************************************************************************************************/  

$(document).ready(function(){
  
	//Function to bring up user data for either delete or update
	$("#userstable tr").click(function(){
        	var modalData = [];

		//load in data from row for the users modal which the user clicked on. 		
		$(this).find("td").each(function(){
			modalData.push($(this).html());
	        });
		
		//Set the modal form with these properties
		$('#ID').text(modalData[0]);
		$('#editname').val(modalData[1]);
		$('#editemail').val(modalData[2]);
		$('#editimage').val(modalData[4]);
		$('#editregion').val(modalData[5]);
		//Show the modal
		$('#editusers').modal('show');
	});



	//Code to show new user modal	
	$('#newuserbutton1').click(function(){
		$('#createusermodal').modal('show');
	});


	//function to delete user
	$('#deleteuserbutton').click(function(){
        	var userID = $('#ID').text();
		//ajax call to backend web server which reroutes to database
                $.ajax({
                        url: '/admin/API/user/' + userID,
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



	//function to edit user
	$('#updateduserbutton').click(function(){
                //add code to check form values are filled out
                if( $('#editname').val()=="" || $('#edituserpwd').val()=="" || $('#editemail').val()=="", $('#editimage').val()=="", $('#editregion').val()==""){
                        if($('#editname').val()==""){
	                        alert('Please Fill Out User Name.');
                        }
                        else if( $('#edituserpwd').val()==""){
                                alert('Please Fill Out User Password.');
                        }
                        else if ($('#editemail').val() ==""){
                                alert('Please Fill Out User Email.');
                        }
			else if ($('#editimage').val() == ""){
				alert('Please Upload Image');
			}		
			else{
				alert('Please Fill Out Region');
			}


                        return;
                }
                var userID = $('#ID').text();
                var formData = {
			name:$('#editname').val()   ,
                        email: $('#editpwd').val()  ,
                        password:  $('#editemail').val(),
			region: $('#editregion').val(),
			image: $('#editimage').val()

                };
		console.log(formData);
                $.ajax({
                        url: '/admin/API/user/' + userID,
                        data: formData,
                        type:"PUT"

                })
                .done(function(result){
                        alert(result);
			location.reload();
                })

                .fail(function(result){
                        alert(failed);
                });
        });

	
	//function to submit new user request
      //Create new User Button
        $('#createuserbutton').click(function(){
                //add code to check form values are filled out
		if( $('#name').val()=="" || $('#pwd').val()=="" || $('#email').val()=="", $('#image').val()=="", $('#region').val()==""){
                        if($('#name').val()==""){
                                alert('Please Fill Out User Name.');
                        }
                        else if( $('#pwd').val()==""){
                                alert('Please Fill Out User Password.');
                        }
                        else if ($('#email').val() ==""){
                                alert('Please Fill Out User Email.');
                        }
                        else if ($('#image').val() == ""){
                                alert('Please Upload Image');
                        }
                        else{
                                alert('Please Fill Out Region');
                        }
                        return;
                }
		//convert image to base 64
		var origImage = $('#newImage');
		if(!origImage){
			alert('Message Failed to Upload');
			return;
		}
			
		alert(origImage.prop('src'));
		//serialize form data
                var formData  = "password=" + $('#pwd').val() + "&uuID=" + $('#name').val() + "&email=" + $('#email').val() + "&signatureImage=" + "comingsoon"  +  "&region=" + $('#region').val() + "&name=" +  $('#name').val() + "&image=" + origImage.prop('src');
                console.log(formData);
		 $.ajax({
                        url: '/admin/API/user',
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
                });

	});


		
});
