## Bruno Vieira Ribeiro - October, 2022
## ICT 128 - Project Phase II
## Script to create MySQL database

## Modules used:
## - mysql.connector -> to interact with the database
#################################################################
## Reference for granting database access
## Grant acces to bruno@localhost: https://stackoverflow.com/questions/37239970/connect-to-mysql-server-without-sudo

import mysql.connector

#################################################################
### Creating the database
#################################################################

mydb = mysql.connector.connect(host="localhost", user="bruno")

print(mydb)

# Creating the database
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE ict128")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)

#################################################################
### Creating tables
#################################################################

# Connecting to database
mydb = mysql.connector.connect(host="localhost", user="bruno", database="ict128")

mycursor = mydb.cursor()

create_country = """
CREATE TABLE IF NOT EXISTS `COUNTRY` (
  `CT_CODE` VARCHAR(3),
  `ct_name` VARCHAR(100) NOT NULL,
  `continent` VARCHAR(10) NOT NULL,
  `currency` VARCHAR(4) NOT NULL,
  PRIMARY KEY (`CT_CODE`)
);
"""

create_account = """
CREATE TABLE IF NOT EXISTS `ACCOUNT` (
  `ACC_ID` INT AUTO_INCREMENT,
  `CT_CODE` VARCHAR(3) NOT NULL,
  `plan` VARCHAR(9) NOT NULL,
  `password` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`ACC_ID`),
  FOREIGN KEY (`CT_CODE`) REFERENCES `COUNTRY`(`CT_CODE`)
);
"""

create_customer = """
CREATE TABLE IF NOT EXISTS `CUSTOMER` (
  `CX_ID` INT AUTO_INCREMENT,
  `ACC_ID` INT NOT NULL,
  `f_name` VARCHAR(20) NOT NULL,
  `l_name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`CX_ID`),
  FOREIGN KEY (`ACC_ID`) REFERENCES `ACCOUNT`(`ACC_ID`)
);
"""

create_distributor = """
CREATE TABLE IF NOT EXISTS `DISTRIBUTOR` (
  `DIS_ID` INT AUTO_INCREMENT,
  `CT_CODE` VARCHAR(3) NOT NULL,
  PRIMARY KEY (`DIS_ID`),
  FOREIGN KEY (`CT_CODE`) REFERENCES `COUNTRY`(`CT_CODE`)
);
"""

create_content = """
CREATE TABLE IF NOT EXISTS `CONTENT` (
  `C_ID` INT AUTO_INCREMENT,
  `DIS_ID` INT NOT NULL,
  `last_viewed` DATETIME,
  `type` VARCHAR(20),
  `tier` VARCHAR(9) NOT NULL,
  `description` TEXT,
  `genre` VARCHAR(20),
  PRIMARY KEY (`C_ID`),
  FOREIGN KEY (`DIS_ID`) REFERENCES `DISTRIBUTOR`(`DIS_ID`)
);
"""

create_date = """
CREATE TABLE IF NOT EXISTS `DATE_KEEP` (
  `D_ID` INT,
  `date_time` DATETIME NOT NULL,
  PRIMARY KEY (`D_ID`)
);
"""

create_pt = """
CREATE TABLE IF NOT EXISTS `PAYMENT_TYPE` (
  `PT_ID` INT AUTO_INCREMENT,
  `type` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`PT_ID`)
);
"""

create_stream = """
CREATE TABLE IF NOT EXISTS `STREAM` (
  `S_ID` INT AUTO_INCREMENT,
  `ACC_ID` INT NOT NULL,
  `C_ID` INT NOT NULL,
  `P_ID` INT,
  `D_ID` INT NOT NULL,
  `perc_watched` INT NOT NULL,
  `star_rate` INT,
  PRIMARY KEY (`S_ID`),
  FOREIGN KEY (`C_ID`) REFERENCES `CONTENT`(`C_ID`),
  FOREIGN KEY (`D_ID`) REFERENCES `DATE_KEEP`(`D_ID`),
  FOREIGN KEY (`ACC_ID`) REFERENCES `ACCOUNT`(`ACC_ID`)
);
"""

create_payment = """
CREATE TABLE IF NOT EXISTS `PAYMENT` (
  `P_ID` INT AUTO_INCREMENT,
  `ACC_ID` INT NOT NULL,
  `PT_ID` INT NOT NULL,
  `D_ID` INT NOT NULL,
  `amount` DECIMAL(6,2) NOT NULL,
  `purpose` VARCHAR(10) NOT NULL,
  `success` BOOL NOT NULL,
  `expiration` DATE,
  PRIMARY KEY (`P_ID`),
  FOREIGN KEY (`ACC_ID`) REFERENCES `ACCOUNT`(`ACC_ID`),
  FOREIGN KEY (`D_ID`) REFERENCES `DATE_KEEP`(`D_ID`),
  FOREIGN KEY (`PT_ID`) REFERENCES `PAYMENT_TYPE`(`PT_ID`)
);
"""


create_av = """
CREATE TABLE IF NOT EXISTS `AVAILABILITY` (
  `C_ID` INT NOT NULL,
  `CT_CODE` VARCHAR(3) NOT NULL,
  `available` BOOL NOT NULL,
  `available_date` DATE,
  `price` DECIMAL(5,2),
  PRIMARY KEY (C_ID, CT_CODE),
  FOREIGN KEY (`CT_CODE`) REFERENCES `COUNTRY`(`CT_CODE`),
  FOREIGN KEY (`C_ID`) REFERENCES `CONTENT`(`C_ID`)
);
"""

create_contacts = """
CREATE TABLE IF NOT EXISTS `CONTACTS` (
  `CONTACT_ID` INT AUTO_INCREMENT,
  `DIS_ID` INT NOT NULL,
  `f_name` VARCHAR(20) NOT NULL,
  `l_name` VARCHAR(50) NOT NULL,
  `location` VARCHAR(20),
  `dept` VARCHAR(20),
  `email` VARCHAR(100) NOT NULL,
  `phone#` INT NOT NULL,
  PRIMARY KEY (`CONTACT_ID`),
  FOREIGN KEY (`DIS_ID`) REFERENCES `DISTRIBUTOR`(`DIS_ID`)
);
"""

erd_execution = [
    create_country,
    create_account,
    create_customer,
    create_distributor,
    create_content,
    create_date,
    create_pt,
    create_stream,
    create_payment,
    create_av,
    create_contacts,
]
for ex in erd_execution:
    mycursor.execute(ex)
    print("Done", ex)

# #################################################################
# ### Checking if tables exist
# #################################################################

mydb = mysql.connector.connect(host="localhost", user="bruno", database="ict128")
mycursor = mydb.cursor()

# Check if tables exist
mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)

################################################################
# TRIGGERS
################################################################

mydb = mysql.connector.connect(host="localhost", user="bruno", database="ict128")
mycursor = mydb.cursor()

## Trigger for STREAM -> DATE_KEEP
stream_to_date_trigg = """
CREATE TRIGGER stream_date_trigg
    BEFORE INSERT
    ON STREAM FOR EACH ROW
    INSERT INTO DATE_KEEP(D_ID, date_time)
    VALUES(NEW.D_ID,
           FROM_UNIXTIME( UNIX_TIMESTAMP('2010-04-30 14:53:27') + FLOOR(0 + (RAND() * 25920000) ) )
    );
"""

# Execute trigger
mycursor.execute(stream_to_date_trigg)

for x in mycursor:
    print(x)

## Trigger for PAYMENT -> DATE_KEEP

mydb = mysql.connector.connect(host="localhost", user="bruno", database="ict128")
mycursor = mydb.cursor()

stream_to_date_trigg = """
CREATE TRIGGER payment_date_trigg
    BEFORE INSERT
    ON PAYMENT FOR EACH ROW
    INSERT INTO DATE_KEEP(D_ID, date_time)
    VALUES(NEW.D_ID,
           FROM_UNIXTIME( UNIX_TIMESTAMP('2010-04-30 14:53:27') + FLOOR(0 + (RAND() * 25920000) ) )
    );
"""

# Execute trigger
mycursor.execute(stream_to_date_trigg)

for x in mycursor:
    print(x)

# Trigger to prevent more than 4 customers in each account

cx_trigger = """
DELIMITER //
CREATE TRIGGER PreventMoreCustomers BEFORE INSERT ON CUSTOMER
FOR EACH ROW
BEGIN
    IF(
        (SELECT COUNT(*)
         FROM ACCOUNT
         WHERE ACC_ID = NEW.ACC_ID
         GROUP BY ACC_ID) > 4
    ) THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Account maxed out';
    END IF;
END //
DELIMITER ;
"""
# Execute trigger
mycursor.execute(cx_trigger)

#################################################################
## EXTRA CONSTRAINTS
#################################################################

## Plan constraints

mydb = mysql.connector.connect(host="localhost", user="bruno", database="ict128")
mycursor = mydb.cursor()

plan_constraint_acc = """
ALTER TABLE ACCOUNT
ADD CONSTRAINT chk_plan CHECK (plan IN ('free','mid-tier','no-limits'))
"""

# Execute constraint
mycursor.execute(plan_constraint_acc)

tier_constraint_cont = """
ALTER TABLE CONTENT
ADD CONSTRAINT chk_tier CHECK (tier IN ('free','mid-tier','no-limits'))
"""

# Execute constraint
mycursor.execute(tier_constraint_cont)

## Payment type constraints
type_constraint_paytype = """
ALTER TABLE PAYMENT_TYPE
ADD CONSTRAINT chk_paytype CHECK (type IN ('credit', 'debit', 'OPS'))
"""

# Execute constraint
mycursor.execute(type_constraint_paytype)
