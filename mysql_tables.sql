CREATE TABLE `emailbulk` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`searchterm` VARCHAR(100),
	`email` VARCHAR(100),
    `date` VARCHAR(20),
    `time` VARCHAR(20),
	PRIMARY KEY (`ID`)
) ENGINE=MyISAM;

CREATE TABLE `emails` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`searchterm` VARCHAR(100),
	`email` VARCHAR(100),
    `date` VARCHAR(20),
    `time` VARCHAR(20),
	PRIMARY KEY (`ID`)
) ENGINE=MyISAM;