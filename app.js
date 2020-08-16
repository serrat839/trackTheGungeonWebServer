/* Thomas Serrano
 * Webserver for Enter the Gungeon Mod: Track The Gungeon
 * 8/9/2020
 */

"use strict";
const express = require("express");
const multer = require("multer");
const fs = require("fs").promises;
const app = express();

// if serving front-end files in public/
app.use(express.static("public"));
app.use(express.json());
app.use(multer().none())

// if handling different POST formats
// app.use(express.urlencoded({ extended: true }));
// app.use(express.json());
// app.use(multer().none());

// app.get/app.post endpoints
// initial interaction checkpoint. Not really needed tbh
app.get("/track", async(req, res) => {
  res.type("text");
  let user = req.query.user;
  if (user) {
    try {
      res.status(200);
      console.log(user + " is interacting with us!");
      res.send("successful interaction with webserver");
    } catch (err) {
      res.status(500).send("Something went wrong")
    }
  } else {
    res.status(400).send("please specify user!");
  }
})

// POST endpoint where users can send game data
app.post("/runEnd", async(req, res) => {
  res.type("text");
  console.log(req.body);
  let guns = req.body.guns;
  //let passive = req.body.passive;
  //let active = req.body.active;
  // other run metadata???

  if (guns) {
    try {
      console.log("someone is POSTING with us!");
      console.log(guns);
      res.status(200);
      res.send("successful interaction with webserver");
    } catch (err) {
      res.status(500).send("Something went wrong")
    }
  } else {
    res.status(400).send("POST BODY WAS BLANK");
  }
})


// helper functions
const PORT = process.env.PORT || 8000;
app.listen(PORT);
