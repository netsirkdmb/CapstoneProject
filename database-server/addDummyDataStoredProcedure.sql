-- Tell which database to use
USE cs419;

-- Drop stored procedure if it exists
DROP PROCEDURE IF EXISTS spAddDummyData;

DELIMITER $$
-- Start stored procedure
CREATE PROCEDURE spAddDummyData ()
BEGIN

-- insert administrators
INSERT INTO admins (email, password) VALUES ('dhusek@oregonstate.edu', 'k');
INSERT INTO admins (email, password) VALUES ('hallbry@oregonstate.edu', 'b');
INSERT INTO admins (email, password) VALUES ('mccumstw@oregonstate.edu', 'w');


-- insert award types
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Employee of the Week', 1);
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Employee of the Month', 10);
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Employee of the Year', 100);
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Gold Star Employee', 20);


-- insert users
INSERT INTO users (name, email, password, signatureImage, region) VALUES ('Kristen', 'dhusek@oregonstate.edu', 'kd', 'kristen d', 'Washington');
INSERT INTO users (name, email, password, signatureImage, region) VALUES ('Bryant', 'hallbry@oregonstate.edu', 'bh', 'bryant h', 'Washington');
INSERT INTO users (name, email, password, signatureImage, region) VALUES ('William', 'mccumstw@oregonstate.edu', 'wm', 'william m', 'Canada');


-- insert awards
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (1, 2, 1, '2016-10-17 18:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (1, 3, 2, '2016-08-01 13:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 1, 4, '2016-09-01 15:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 3, 1, '2016-10-24 17:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (3, 1, 3, '2016-01-01 14:30:00');

END$$

DELIMITER ;