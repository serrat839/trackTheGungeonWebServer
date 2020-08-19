-- Author: Thomas Serrano
-- Last Updated: 8/8/2020
-- Creates a table containing gungeon run data
CREATE TABLE run_data (
	id					INTEGER PRIMARY KEY AUTOINCREMENT,
	gungeoneer			VARCHAR(15) NOT NULL,
	duration			INTEGER NOT NULL,
	floor				VARCHAR(30) NOT NULL,
	carried_money		INTEGER NOT NULL,
	total_money			INTEGER NOT NULL,
	rainbow				BOOLEAN NOT NULL,
	blessed				BOOLEAN NOT NULL,
	turbo				BOOLEAN NOT NULL,
	challenge			BOOLEAN NOT NULL,
	passive				VARCHAR(4000) NOT NULL,
	active				VARCHAR(1500) NOT NULL,
	guns				VARCHAR(4000) NOT NULL
)