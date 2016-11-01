#API Readme

**API base endpoint:**
http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600


**Admins Table:** [/admins](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins)
- get: returns all admins in the database
- post: creates a new admin in the database
- put: invalid
- delete: deletes all admins in the database


**Admins Table by ID:** [/admins/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins/1)
- get: returns admin with specified id _(specified id is represented by "1234")_
- post: invalid
- put: updates admin with specified id
- delete: deletes admin with specified id


**Users Table:** [/users](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/users)
- get: returns all users in the database (does not include signature image)
- post: creates a new users in the database
- put: invalid
- delete: deletes all users in the database


**Users Table by ID:** [/users/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/users/1)
- get: returns user with specified id _(specified id is represented by "1234")_, includes signature image
- post: invalid
- put: updates user with specified id, signatureImage not required
- delete: deletes user with specified id


**Awards Table:** [/awards](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/awards)
- get: returns all awards in the database
- post: creates a new award in the database
- put: invalid
- delete: deletes all awards in the database


**Awards Table by awardID:** [/awards/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/awards/1)
- get: returns award with specified id _(specified id is represented by "1234")_
- post: invalid
- put: updates award with specified id
- delete: deletes award with specified id


**Awards Table by userID:** [/userAwards/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/userAwards/1)
- get: returns all awards given by user with specified id _(specified id is represented by "1234")_
- post: invalid
- put: invalid
- delete: deletes all awards given by user with specified id


**Award Types Table:** [/awardTypes](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/awardTypes)
- get: returns all award types in the database
- post: creates a new award types in the database
- put: invalid
- delete: deletes all award types in the database


**Award Types Table by ID:** [/awardTypes/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/awardTypes/1)
- get: returns award type with specified id _(specified id is represented by "1234")_
- post: invalid
- put: updates award type with specified id
- delete: deletes award type with specified id


**Reset Tables:** [/resetTables](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/resetTables)
- post: drops all tables in the database and creates them again


**Reset Tables with Dummy Data:** [/resetTablesWithDummyData](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/resetTablesWithDummyData)
- post: drops all tables in the database, creates them again, and adds dummy data

**Get Award Creation Info:** [/getAwardCreationInfo/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getAwardCreationInfo/1)
- get: returns the info required to create the award with the awardID specified, also creates certificate.pdf (currently does test certificate)

**Get User by Email:** [/getUserByEmail](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getUserByEmail)
- post: returns user with specified email (does not include signature image)

**Get Admin by Email:** [/getAdminByEmail](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getAdminByEmail)
- post: returns admin with specified email