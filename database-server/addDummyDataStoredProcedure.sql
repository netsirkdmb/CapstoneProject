-- Tell which database to use
USE cs419;

-- Drop stored procedure if it exists
DROP PROCEDURE IF EXISTS spAddDummyData;

DELIMITER $$
-- Start stored procedure
CREATE PROCEDURE spAddDummyData ()
BEGIN

-- insert administrators
INSERT INTO admins (email, password, salt) VALUES ('dhusek@oregonstate.edu', 'k', '');
INSERT INTO admins (email, password, salt) VALUES ('hallbry@oregonstate.edu', 'b', '');
INSERT INTO admins (email, password, salt) VALUES ('mccumstw@oregonstate.edu', 'w', '');


-- insert award types
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Employee of the Week', 1);
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Employee of the Month', 10);
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Employee of the Year', 100);
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Gold Star Employee', 20);
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Silver Star Employee', 10);


-- insert users
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('Kristen', 'dhusek@oregonstate.edu', 'kd', '', 'kristen d', 'Washington', '2015-07-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('Bryant', 'hallbry@oregonstate.edu', 'bh', '', 'bryant h', 'Washington', '2014-03-02');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('William', 'mccumstw@oregonstate.edu', 'wm', '', 'william m', 'Canada', '2015-09-15');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test1', 'test1@test.com', 'a', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test2', 'test2@test.com', 'b', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test3', 'test3@test.com', 'c', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test4', 'test4@test.com', 'd', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test5', 'test5@test.com', 'e', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test6', 'test6@test.com', 'f', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test7', 'test7@test.com', 'g', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test8', 'test8@test.com', 'h', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test9', 'test9@test.com', 'i', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test10', 'test10@test.com', 'j', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test11', 'test11@test.com', 'k', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test12', 'test12@test.com', 'l', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test13', 'test13@test.com', 'm', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test14', 'test14@test.com', 'n', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test15', 'test15@test.com', 'o', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test16', 'test16@test.com', 'p', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test17', 'test17@test.com', 'q', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test18', 'test18@test.com', 'r', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test19', 'test19@test.com', 's', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test20', 'test20@test.com', 't', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test21', 'test21@test.com', 'u', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test22', 'test22@test.com', 'v', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test23', 'test23@test.com', 'w', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test24', 'test24@test.com', 'x', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test25', 'test25@test.com', 'y', 'abc', '', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test26', 'test26@test.com', 'z', 'abc', '', 'US', '2016-09-30');


-- insert awards
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (1, 2, 1, '2016-10-17 18:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (1, 3, 2, '2016-08-01 13:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 1, 4, '2016-09-01 15:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 3, 1, '2016-10-24 17:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (3, 1, 3, '2016-01-01 14:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (1, 2, 4, '2016-03-17 18:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 3, 1, '2016-03-17 18:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 1, 2, '2016-03-17 18:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (1, 3, 3, '2016-05-01 13:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 1, 3, '2016-07-01 15:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 3, 2, '2016-02-24 17:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (3, 1, 1, '2016-04-01 14:30:00');

END$$

DELIMITER ;