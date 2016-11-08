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

##Business Intelligence Suite Calls
**Top Performing Employees:** [/getTopEmployees](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getTopEmployees)
- get: returns the top 5 performing employees for each month of the previous year as well as the top 5 employees overall for the past year

**Ranking All-Time:** [/getRanking](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getRanking)
- get: returns the overall employee ranking based on awards received all-Time

**Most Generous Employees:** [/getGenerousEmployees](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getGenerousEmployees)
- get: returns the top 5 most generous employees for each month of the previous year as well as the top 5 employees overall for the past year

**Frequency Chart:** [/getFrequencyChart](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getFrequencyChart)
- get: returns the number of awards given each month for the previous 12 months

**Award Types:** [/getAwardTypes](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getAwardTypes)
- get: returns the types of awards given over the previous 12 months

**Employee Ranking:** [/getRanking/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getRanking/1)
- get: returns overall ranking of the employee with specified id _(specified id is represented by "1234")_

**Employee Prestige Points:** [/getPrestigePoints/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getPrestigePoints/1)
- get: returns total points earned by the employee with specified id _(specified id is represented by "1234")_ in each month of their career

**Employee Award Types:** [/getAwardTypes/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getAwardTypes/1)
- get: returns types of awards earned by the employee with specified id _(specified id is represented by "1234")_ over their career

**Employee Awards Received:** [/getAwardsReceived/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getAwardsReceived/1)
- get: returns the awards that the employee with specified id _(specified id is represented by "1234")_ has received over their career

**Employee Award Giving Frequency:** [/getAwardsGivenFrequency/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getAwardsGivenFrequency/1)
- get: returns the number of awards the employee with specified id _(specified id is represented by "1234")_ has given in each month of their career

**Employee Types of Awards Given:** [/getAwardTypesGiven/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/getAwardTypesGiven/1)
- get: returns the types of awards that the employee with specified id _(specified id is represented by "1234")_ has given along with their Frequency

**Employee Awards Given:** [/userAwards/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/userAwards/1)
- get: returns all awards given by employee with specified id _(specified id is represented by "1234")_