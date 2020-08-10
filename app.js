"use strict";
/* Thomas Serrano
 * Webserver for Enter the Gungeon Mod: Track The Gungeon
 * 8/9/2020
 */

const express = require("express");
const multer = require("multer");
// other modules you use
// program constants
const app = express();

// if serving front-end files in public/
app.use(express.static("public"));

// if handling different POST formats
// app.use(express.urlencoded({ extended: true }));
// app.use(express.json());
// app.use(multer().none());

// app.get/app.post endpoints
app.get("/track", async(req, res) => {
  res.type("text");
  let user = req.query.user;
  if (user) {
    try {
      res.status(200);
      console.log("someone is interacting with us!");
      console.log(user + " is interacting with us!");
      res.send("successful interaction with webserver");
    } catch (err) {
      res.status(500).send("Something went wrong")
    }
  } else {
    res.status(400).send("please specify user!");
  }
})

// helper functions
const PORT = process.env.PORT || 8000;
app.listen(PORT);
