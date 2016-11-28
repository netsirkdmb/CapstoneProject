function readURL(input){
	if(input.files && input.files[0]){
		var reader = new FileReader();
		reader.onload = function(e){
			$('#newImage')
				.attr('src', e.target.result)
				.width(150)
				.height(150);

		};
		reader.readAsDataURL(input.files[0]);
	}
};



function editURL(input){
        if(input.files && input.files[0]){
                var reader = new FileReader();
                reader.onload = function(e){
                        $('#editimagepic')
                                .attr('src', e.target.result)
                                .width(150)
                                .height(150);

                };
                reader.readAsDataURL(input.files[0]);
        }
};

