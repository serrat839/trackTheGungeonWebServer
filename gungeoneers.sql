-- Author: Thomas Serrano
-- Last Updated: 8/8/2020
-- Creates a table containing the different pseudonyms for gungeoneers
CREATE TABLE gungeon_names (
	codename	VARCHAR(30) NOT NULL,
	name		VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO gungeon_names (codename, name) VALUES ("Bullet", "The Bullet");
INSERT INTO gungeon_names (codename, name) VALUES ("Guide", "The Hunter");
INSERT INTO gungeon_names (codename, name) VALUES ("Eevee", "The Paradox");
INSERT INTO gungeon_names (codename, name) VALUES ("Soldier", "The Marine");
INSERT INTO gungeon_names (codename, name) VALUES ("Pilot", "The Pilot");
INSERT INTO gungeon_names (codename, name) VALUES ("Convict", "The Convict");
INSERT INTO gungeon_names (codename, name) VALUES ("Robot", "The Robot");