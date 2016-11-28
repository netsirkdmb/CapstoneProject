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

		//set up ajax call for user data


		//load in data from row for the users modal which the user clicked on. 		
		$(this).find("td").each(function(){
			modalData.push($(this).html());
	        });

		//ajax call 
		$.ajax({
			url: '/admin/API/user/' + modalData[0]
		}).done(function(result){
			var jsonResult = JSON.parse(result);
			var date = new Date(jsonResult.Data[0].startDate);
			$('#ID').text(jsonResult.Data[0].userID);
			$('#editname').val(jsonResult.Data[0].name);
                	$('#editemail').val(jsonResult.Data[0].email);
			$('#editregion').val(jsonResult.Data[0].region);
			$('#editdatepicker').val(date);
			$('#editusers').modal('show');
			//get image from server
			 $('#editimagepic')
                                .attr('src', '/admin/API/images?url=' + jsonResult.Data[0].signatureImage)
                                .width(150)
                                .height(150);

		}).error(function(err){
			console.log(err);
			alert("Error Retrieving User Data");		
		});
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
			alert(result);
			location.reload();			
                })
                .fail(function(result){
                        alert('Failed: ' + result);
                });
        });



	//function to edit user
	$('#updateduserbutton').click(function(){
                //add code to check form values are filled out
                
	

		if( $('#editname').val()== "" || $('#editpwd').val()==""  || $('#editemail').val()=="" || $('#editimage').val() == "" ||   $('#editregion').val()=="" || $('#editdatepicker').val == ""){
                        if($('#editname').val()==""){
	                        alert('Please Fill Out User Name.');
                        }
                        else if( $('#editpwd').val()==""){
                                alert('Please Fill Out User Password.');
                        }
                        else if ($('#editemail').val() ==""){
                                alert('Please Fill Out User Email.');
                        }
	
			else if ($('#editdatepicker').val() ==""){
                                alert('Please Fill Out A Start Date.');

                        }

			else if ($('#editimage').val() ==""){
                                alert('Please Upload a New Image.');
                        }

			else{
				alert('Please Fill Out Region');
			}


                        return;
                }
		//validate email is correct
		if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($('#editemail').val())){
			alert("Invalid Email Address");
			return;
		}
		
		//validate image type is support
		if(!(/^.*\.(jpg|jpeg|JPG|png|PNG)$/.test($('#editimage').val()))){
			alert("Please Attach a jpeg or png");
			return;
		};
	

                var userID = $('#ID').text();
                var testData = new FormData();


              //convert image to base 64
                var origImage = $('#newImage');
                if(!origImage){
                        alert('Message Failed to Upload');
                        return;
                }


                var testData = new FormData();

                testData.append('password', $('#editpwd').val());
                testData.append('email', $('#editemail').val());
                testData.append('name', $('#editname').val());
                testData.append('region',  $('#editregion').val());
                testData.append('startDate',  $('#editdatepicker').val());
		//Add new Signature Image
		var files = $('#editimage')[0].files[0];

		 testData.append('avatar', files, files.name);

                $.ajax({
                        url: '/admin/API/user/' + userID,
                        type:"PUT",
                        dataType: 'json',
                        cache: false,
                        processData: false,
                        contentType: false,
                        data: testData
                })
                .done(function(result){
                        alert(result.result);
			location.reload();
                })

                .fail(function(result){
                        alert(failed);
                });
        });

	
	//function to submit new user request
      //Create new User Button
        $('#createuserbutton').click(function(){

		console.log("test");
                //add code to check form values are filled out
		if( $('#name').val()=="" || $('#pwd').val()=="" || $('#email').val()=="", $('#image').val()=="", $('#region').val()=="", $('#datepicker').val() == ""){
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
			else if($('#datepicker').val() == ""){
				alert("Please Pick a Start Date");
			}
  
			else if($('#region').val() == ""){
                                alert("Please Pick a Region");
                        }

	                else{
                                alert('Please Fill Out Region');
                        }
                        return;
                }
		//validate email is correct
                if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($('#email').val())){
                        alert("Invalid Email Address");
                        return;
                }

	       //validate image type is support
                if(!(/^.*\.(jpg|jpeg|JPG|png|PNG)$/.test($('#image').val()))){
                        alert("Please Attach a jpeg or png");
                        return;
                };


		
		var origImage = $('#newImage');
		if(!origImage){
			alert('Message Failed to Upload');
			return;
		}
			
		//serialize form data
		var files = $('input[type=file]')[0].files[0];
		
		var testData = new FormData();
		
		testData.append('password', $('#pwd').val());
		testData.append('email', $('#email').val());
		testData.append('name', $('#name').val());
		testData.append('region',  $('#region').val());
		testData.append('startDate',  $('#datepicker').val());

		testData.append('avatar', files, files.name);
		console.log(testData);

		 $.ajax({
                        url: '/admin/API/user',
			dataType: 'json',
			cache: false,
			processData: false,
			contentType: false,
                        type: "POST",
			data: testData
                })

                .done(function(result){
                        console.log(result);
                        if(result.Status == 400) {
                                alert('Bad Request');
                        }
                        else{
                                alert(result.result);
                                location.reload();
                        }

                });

	});
});
