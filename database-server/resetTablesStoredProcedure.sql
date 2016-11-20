-- Tell which database to use
USE cs419;

-- Drop stored procedure if it exists
DROP PROCEDURE IF EXISTS spResetTables;

DELIMITER $$
-- Start stored procedure
CREATE PROCEDURE spResetTables ()
BEGIN

-- Drop all tables to reset database
	DROP TABLE IF EXISTS admins;
	DROP TABLE IF EXISTS awards;
	DROP TABLE IF EXISTS awardTypes;
	DROP TABLE IF EXISTS users;


-- Create a table called admins with the following properties:
-- adminID - an auto incrementing integer which is the primary key
-- email - a varchar with a maximum length of 255 characters, cannot be null, must be unique
-- password - a varchar with a maximum length of 255 characters, cannot be null
-- salt - a varchar with a maximum length of 255 characters, cannot be null, must be unique
-- accountCreationTime - the datetime that this record was first created, cannot be null
	CREATE TABLE admins (
		adminID INT AUTO_INCREMENT,
		email VARCHAR(255) NOT NULL UNIQUE,
		password VARCHAR(512) NOT NULL,
		salt VARCHAR(16) NOT NULL UNIQUE,
		accountCreationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY(adminID)
	) ENGINE=InnoDB;


-- Create a table called users with the following properties:
-- userID - an auto incrementing integer which is the primary key
-- name - a varchar with a maximum length of 255 characters, cannot be null
-- email - a varchar with a maximum length of 255 characters, cannot be null, must be unique
-- password - a varchar with a maximum length of 255 characters, cannot be null
-- salt - a varchar with a maximum length of 255 characters, cannot be null, must be unique
-- passwordCode - a varchar with a maximum length of 255 characters, default is null
-- signatureImage - a varchar with a maximum length of 255 characters, default is null
-- region - a varchar with a maximum length of 255 characters, cannot be null
-- startDate - the date that this user started, cannot be null
-- accountCreationTime - the datetime that this record was first created, cannot be null
	CREATE TABLE users (
		userID INT AUTO_INCREMENT,
		name VARCHAR(255) NOT NULL,
		email VARCHAR(255) NOT NULL UNIQUE,
		password VARCHAR(255) NOT NULL,
		salt VARCHAR(16) NOT NULL UNIQUE,
		passwordCode VARCHAR(255) DEFAULT NULL,
		signatureImage VARCHAR(255) DEFAULT NULL,
		region VARCHAR(255) NOT NULL,
		startDate DATE NOT NULL,
		accountCreationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY(userID)
	) ENGINE=InnoDB;


-- Create a table called awardTypes with the following properties:
-- awardTypeID - an auto incrementing integer which is the primary key
-- name - a varchar with a maximum length of 255 characters, cannot be null, must be unique
-- prestigeLevel - an integer which must be positive, cannot be null
	CREATE TABLE awardTypes (
		awardTypeID INT AUTO_INCREMENT,
		name VARCHAR(255) NOT NULL UNIQUE,
		prestigeLevel INT UNSIGNED NOT NULL,
		PRIMARY KEY(awardTypeID)
	) ENGINE=InnoDB;


-- Create a table called awards with the following properties:
-- awardID - an auto incrementing integer which is the primary key
-- receiverID - an integer which is a foreign key reference to the users table, cannot be null
-- giverID - an integer which is a foreign key reference to the users table, cannot be null
-- typeID - an integer which is a foreign key reference to the awardType table, cannot be null
-- datetimeGranted - the datetime that this award was given, cannot be null
-- awardDate - the date and time that the award is for, cannot be null
	CREATE TABLE awards (
		awardID INT AUTO_INCREMENT,
		receiverID INT NOT NULL,
		giverID INT NOT NULL,
		typeID INT NOT NULL,
		datetimeGranted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		awardDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY(awardID),
		CONSTRAINT receiverID
			FOREIGN KEY(receiverID)
			REFERENCES users(userID)
			ON UPDATE CASCADE
			ON DELETE CASCADE,
		CONSTRAINT giverID
			FOREIGN KEY(giverID)
			REFERENCES users(userID)
			ON UPDATE CASCADE
			ON DELETE CASCADE,
		CONSTRAINT typeID
			FOREIGN KEY(typeID)
			REFERENCES awardTypes(awardTypeID)
			ON UPDATE CASCADE
			ON DELETE CASCADE
	) ENGINE=InnoDB;

END$$

DELIMITER ;