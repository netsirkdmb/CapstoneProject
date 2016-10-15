#API Readme

**API base endpoint:**
http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600

**Admins Table:** [/admins](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins)
- get: returns all admins in the database
- post: creates a new admin in the database
- put: invalid
- delete: deletes all admins in the database

**Admins Table by ID:** [/admins/1234](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/admins/1)
- get: returns admin with specified id
- post: invalid
- put: updates admin with specified id
- delete: deletes admin with specified id

**Reset Tables:** [/resetTables](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/resetTables)
- drops all tables in the database and creates them again

**Reset Tables with Dummy Data:** [/resetTablesWithDummyData](http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/resetTablesWithDummyData)
- drops all tables in the database, creates them again, and adds dummy data
