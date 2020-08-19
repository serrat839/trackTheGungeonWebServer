/* Thomas Serrano
 * Webserver for Enter the Gungeon Mod: Track The Gungeon
 * 8/9/2020
 */

"use strict";
const express = require("express");
const multer = require("multer");
const sqlite3 = require("sqlite3");
const sqlite = require("sqlite")

const app = express();

// if serving front-end files in public/
//app.use(express.static("public"));
app.use(express.json());
app.use(multer().none());

// POST endpoint where users can send game data
app.post("/runEnd", async(req, res) => {
  res.type("text");
  if (req.body) {
    try {
      // use db.run to insert the data bc that is for inserting data, does not return stuff.
      // db.all returns stuff
      let db = await getDBConnection();
      let qry = `INSERT INTO run_data (gungeoneer, schema, duration, floor, kills, carried_money, total_money,
        rainbow, blessed, turbo, challenge, passive, active, guns, isVictory) VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);`;

      await db.run(qry,
        req.body.metadata.gungeoneer,
        req.body.schema,
        parseInt(req.body.metadata.duration),
        req.body.metadata.floor,
        parseInt(req.body.metadata.kills),
        parseInt(req.body.metadata.carried_money),
        parseInt(req.body.metadata.total_money),
        req.body.metadata.rainbow.toLowerCase() === "true",
        req.body.metadata.blessed.toLowerCase() === "true",
        req.body.metadata.turbo.toLowerCase() === "true",
        req.body.metadata.challenge.toLowerCase() === "true",
        "[" + req.body.passive.toString() + "]",
        "[" + req.body.active.toString() + "]",
        "[" + req.body.guns.toString() + "]",
        req.isVictory.toLowerCase() === "true"
      );

      console.log("submitted to db");
      await db.close()
      res.status(200);
      res.send("successful interaction with webserver");
    } catch (err) {
      console.log(err);
      res.status(500).send("Something went wrong")
    }
  } else {
    res.status(400).send("POST BODY WAS BLANK");
  }
});


/* Establishes a database connection to the wpl database and returns the database object.
 * Any errors that occur during connection should be caught in the function
 * that calls this one.
 * @returns {Object} - The database object for the connection.
 */
async function getDBConnection() {
    const db = await sqlite.open({
        filename: 'gungeon.db',
        driver: sqlite3.Database
    });

    return db;
};

// helper functions
const PORT = process.env.PORT || 8000;
app.listen(PORT);
