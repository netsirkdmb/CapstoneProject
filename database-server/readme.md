#API Readme

**API base endpoint:**
http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600

**API base endpoint for HTTPS:**
https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com


**Admins Table:** [/admins](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/admins)
- get: returns all admins in the database
- post: creates a new admin in the database
- put: invalid
- delete: deletes all admins in the database


**Admins Table by ID:** [/admins/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/admins/1)
- get: returns admin with specified id _(specified id is represented by "1234")_
- post: invalid
- put: updates admin with specified id
- delete: deletes admin with specified id


**Users Table:** [/users](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/users)
- get: returns all users in the database (does not include signature image)
- post: creates a new users in the database
- put: invalid
- delete: deletes all users in the database


**Users Table by ID:** [/users/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/users/1)
- get: returns user with specified id _(specified id is represented by "1234")_, includes signature image
- post: invalid
- put: updates user with specified id, signatureImage not required
- delete: deletes user with specified id


**Awards Table:** [/awards](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/awards)
- get: returns all awards in the database
- post: creates a new award in the database
- put: invalid
- delete: deletes all awards in the database


**Awards Table by awardID:** [/awards/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/awards/1)
- get: returns award with specified id _(specified id is represented by "1234")_
- post: invalid
- put: updates award with specified id
- delete: deletes award with specified id


**Awards Given by userID:** [/userAwards/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/userAwards/1)
- get: returns all awards given by user with specified id _(specified id is represented by "1234")_
- post: invalid
- put: invalid
- delete: deletes all awards given by user with specified id


**Award Types Table:** [/awardTypes](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/awardTypes)
- get: returns all award types in the database
- post: creates a new award types in the database
- put: invalid
- delete: deletes all award types in the database


**Award Types Table by ID:** [/awardTypes/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/awardTypes/1)
- get: returns award type with specified id _(specified id is represented by "1234")_
- post: invalid
- put: updates award type with specified id
- delete: deletes award type with specified id


**Create Award PDF:** [/createAwardPDF/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/createAwardPDF/1)
- get: returns the info required to create the award with the awardID specified, also creates and emails certificate.


**Get User by Email:** [/getUserByEmail](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getUserByEmail)
- post: returns user with specified email (does not include signature image)


**Get Admin by Email:** [/getAdminByEmail](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getAdminByEmail)
- post: returns admin with specified email



##Business Intelligence Suite Calls
**Top Performing Employees:** [/getTopEmployees](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getTopEmployees)
- get: returns the top 5 performing employees for each month of the previous year as well as the top 5 employees overall for the past year


**Ranking All-Time:** [/getRanking](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getRanking)
- get: returns the overall employee ranking based on awards received all-Time


**Most Generous Employees:** [/getGenerousEmployees]https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getGenerousEmployees)
- get: returns the top 5 most generous employees for each month of the previous year as well as the top 5 employees overall for the past year


**Frequency Chart:** [/getFrequencyChart](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getFrequencyChart)
- get: returns the number of awards given each month for the previous 12 months


**Award Types:** [/getAwardTypes](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getAwardTypes)
- get: returns the types of awards given over the previous 12 months


**Employee Ranking:** [/getRanking/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getRanking/1)
- get: returns overall ranking of the employee with specified id _(specified id is represented by "1234")_


**Employee Prestige Points:** [/getPrestigePoints/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getPrestigePoints/1)
- get: returns total points earned by the employee with specified id _(specified id is represented by "1234")_ in each month of their career


**Employee Award Types:** [/getAwardTypes/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getAwardTypes/1)
- get: returns types of awards earned by the employee with specified id _(specified id is represented by "1234")_ over their career


**Employee Awards Received:** [/getAwardsReceived/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getAwardsReceived/1)
- get: returns the awards that the employee with specified id _(specified id is represented by "1234")_ has received over their career


**Employee Award Giving Frequency:** [/getAwardsGivenFrequency/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getAwardsGivenFrequency/1)
- get: returns the number of awards the employee with specified id _(specified id is represented by "1234")_ has given in each month of their career


**Employee Types of Awards Given:** [/getAwardTypesGiven/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/getAwardTypesGiven/1)
- get: returns the types of awards that the employee with specified id _(specified id is represented by "1234")_ has given along with their Frequency


**Employee Awards Given:** [/userAwards/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/userAwards/1)
- get: returns all awards given by employee with specified id _(specified id is represented by "1234")_



##Maintenance Endpoints
_These endpoints are only to be used for database maintenance and NOT for the website!_


**Reset Tables:** [/resetTables](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/resetTables)
- post: drops all tables in the database and creates them again


**Reset Tables with Dummy Data:** [/resetTablesWithDummyData](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/resetTablesWithDummyData)
- post: drops all tables in the database, creates them again, and adds dummy data


**Upload Signature Image:** [/uploadSignatureImage/1234](https://ec2-52-42-152-172.us-west-2.compute.amazonaws.com/uploadSignatureImage/1)
- post: uploads a signature image for the employee with specified id _(specified id is represented by "1234")_