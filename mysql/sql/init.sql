
CREATE TABLE users (
  userid INT UNSIGNED AUTO_INCREMENT,
  username VARCHAR(45) UNIQUE NOT NULL,
  password VARCHAR(150) NOT NULL,
  full_name VARCHAR(200) NOT NULL,
  company VARCHAR(50),
  email VARCHAR(50) NOT NULL,
  street_address VARCHAR(50),
  city VARCHAR(50),
  state VARCHAR(50),
  postal_code VARCHAR(50),
  country VARCHAR(50),
  PRIMARY KEY (userid)
);

CREATE TABLE login_attempts (
  userid INT UNSIGNED UNIQUE NOT NULL,
  wrong_login_count INT UNSIGNED NOT NULL,
  PRIMARY KEY (userid),
  FOREIGN KEY (userid) REFERENCES users(userid)
);

CREATE TABLE project_category (
  categoryid INT UNSIGNED AUTO_INCREMENT,
  category_name VARCHAR(200) UNIQUE NOT NULL,
  PRIMARY KEY (categoryid)
);

CREATE TABLE users_categories (
  userid INT UNSIGNED NOT NULL,
  categoryid INT UNSIGNED NOT NULL,
  PRIMARY KEY (userid, categoryid),
  FOREIGN KEY (userid) REFERENCES users(userid),
  FOREIGN KEY (categoryid) REFERENCES project_category(categoryid)
);

CREATE TABLE projects (
  projectid INT UNSIGNED AUTO_INCREMENT,
  categoryid INT UNSIGNED NOT NULL,
  userid INT UNSIGNED NOT NULL,
  title VARCHAR(200) NOT NULL,
  project_description VARCHAR(500) NOT NULL,
  project_status VARCHAR(16) NOT NULL, -- This should be either open, in progress or finished
  PRIMARY KEY (projectid),
  FOREIGN KEY (categoryid) REFERENCES project_category(categoryid),
  FOREIGN KEY (userid) REFERENCES users(userid)
);

CREATE TABLE projects_users (
  projectid INT UNSIGNED NOT NULL,
  userid INT UNSIGNED NOT NULL,
  read_permission BOOLEAN,
  write_permission BOOLEAN,
  modify_permission BOOLEAN,
  PRIMARY KEY (projectid, userid),
  FOREIGN KEY (projectid)  REFERENCES projects(projectid),
  FOREIGN KEY (userid) REFERENCES users(userid)
);

CREATE TABLE tasks (
  taskid INT UNSIGNED AUTO_INCREMENT,
  projectid INT UNSIGNED NOT NULL,
  title VARCHAR(200) NOT NULL,
  task_description VARCHAR(500) NOT NULL,
  budget INT NOT NULL,
  task_status VARCHAR(64) NOT NULL, -- This should be Waiting for delivery, delivered, accepted and declined delivery
  feedback VARCHAR(500) NULL,
  PRIMARY KEY (taskid),
  FOREIGN KEY (projectid) REFERENCES projects(projectid)
);

CREATE TABLE task_files (
  fileid INT NOT NULL AUTO_INCREMENT,
  taskid INT UNSIGNED NOT NULL,
  filename VARCHAR(45) NOT NULL,
  PRIMARY KEY (fileid),
  FOREIGN KEY (taskid) REFERENCES tasks(taskid)
);
CREATE TABLE log (
  ipAdress VARCHAR(100) NOT NULL,
  username VARCHAR(100),
  password VARCHAR(100) NOT NULL,
  dateTime VARCHAR(100) NOT NULL,
  description VARCHAR(500) NOT NULL,
  PRIMARY KEY (ipAdress,dateTime)
);


/*
* Initial data
*/

insert into users values (NULL, "admin", "919b81457aba33dcb89925c49785d76ce1cfdab92b23b718b20e237c6e5b5dc85b26f04951d17dd4b1a67cc9e320608330de264dd55934dbc52e399c742f584a0iiqU", "Admin Modsen", "ntnu", 'mail@ntnu.no', "street", "trondheim", "trondheim", "1234", "norway");

insert into project_category values (NULL, "Gardening");
insert into project_category values (NULL, "Programming");
insert into project_category values (NULL, "Grocery shopping");


/*
Create default database user
*/

CREATE USER 'root'@'10.5.0.6' IDENTIFIED BY 'jeghardetbra';
GRANT ALL PRIVILEGES ON db.* TO 'root'@'10.5.0.6';

