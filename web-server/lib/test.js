


var fs = require('fs');
var request = require('request');


var formData = {
        image: fs.createReadStream('uploads/2f33d8cb0c16e5c42192663e75894d0e'),

        password: 'sdfsd',
        email:  'junk1@gmail.com',
        salt: '43242fsdsdf'   ,
        region: 'us',
        name: 'test',
        startDate: '2016/11/11'
};
request.post({url:'http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/users', formData: formData}, function optionalCallback(err, httpResponse, body) {
  if (err) {
    return console.error('upload failed:', err);
  }
  console.log('Upload successful!  Server responded with:', body);
});


