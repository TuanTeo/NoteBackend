# Python REST API CRUD Example using Flask and MySQL

### Step 1. 
Create the below *app.py script(py is the extension to indicate Python script) where we import the flask module. This file should be created under user_crud directory. Notice how we create flask instance. 

### Step 2. 
We create the below *db_config.py Python script under user_crud to setup the MySQL database configurations for connecting to database. We need to configure database connection with flask module and that’s why we have imported app module and setup the MySQL configuration with flask module.

### Step 3. 
Next we need *main.py script under *user_crud directory. This script is the perfect instance of Python REST API CRUD Example using Flask and MySQL. It defines all REST URIs for performing CRUD operations. It will also connect to *MySQL database server and query the database to read, insert, update and delete.
Here you can use http PUT method and http DELETE method for updating and deleting users respectively. I have defined only 404 method to handle not found error. You should basically handle required errors, such as, server errors for http responses 500, occurred during the REST API calls.

### Step 4. 
Create MySQL database table — tbl_user with the following structure.

  CREATE TABLE `tbl_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_email` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_password` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `avatar` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `display_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`user_id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `tbl_task` (
  `task_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `modify_time` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` TEXT COLLATE utf8_unicode_ci DEFAULT NULL,
  `pin_enable` BOOL DEFAULT 0,
  `is_archived` BOOL DEFAULT 0,
  `is_deleted` BOOL DEFAULT 0,
  `delete_date` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`task_id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `tbl_detail` (
  `detail_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `modify_time` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `content` TEXT COLLATE utf8_unicode_ci DEFAULT NULL,
  `files` TEXT COLLATE utf8_unicode_ci DEFAULT NULL,
  `index` INT,
  `is_done` BOOL DEFAULT 0,
  `is_deleted` BOOL DEFAULT 0,
  `task_id` bigint(20) NOT NULL,
  PRIMARY KEY (`detail_id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `tbl_biometric` (
  `session_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` TEXT COLLATE utf8_unicode_ci DEFAULT NULL,
  `public_key` TEXT COLLATE utf8_unicode_ci DEFAULT NULL,
  `c` TEXT COLLATE utf8_unicode_ci DEFAULT NULL,
  `h` TEXT COLLATE utf8_unicode_ci DEFAULT NULL,
  `u` TEXT COLLATE utf8_unicode_ci DEFAULT NULL,
  `g` TEXT COLLATE utf8_unicode_ci DEFAULT NULL,
  `z` TEXT COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`session_id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
  

## Testing the Application (Use Postman For Testing)
* Display all users
  GET http://localhost:5000/users
* Add new user
  POST http://localhost:5000/add
  
  {
	"name":"Soumitra",
	"email":"contact@roytuts.com",
	"pwd":"pwd"
  }
  
 * Response : “User added successfully!”
 * Cmd Command : python main.py

````angular2html
flask --app main.py --debug run
````

## Cách dùng MySQL
````
mysql -u note -p123456788
````
````angular2html
use note_db;
````
````angular2html
SHOW TABLES;
````
Các table trong DB
````angular2html
tbl_user, tbl_note, tbl_detal, tbl_biometric
````
````
DROP TABLE NAME;
````
````angular2html
SELECT * FROM tbl_user;
````
````angular2html
INSERT INTO tbl_user(user_name, user_email, user_password) VALUES('tuanteo', 'tuantqt0108@gmail.com', '123456a@');
````
````angular2html
UPDATE tbl_task SET title=%s, pin_enable=%s, is_deleted=%s WHERE task_id=%s
````
````angular2html
DELETE FROM tbl_user WHERE user_id=%s
````