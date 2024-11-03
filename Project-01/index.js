// import express from "express";
// import users from "./MOCK_DATA.json";

const express = require("express");
const users = require("./MOCK_DATA.json");
const fs = require("fs");
const mongo = require("mongoose");
const { type } = require("os");

const app = express();
const PORT = 1906;

app.use(express.urlencoded({ extended: false }));

app.use(express.json());

// Schema
const userSchema = new mongo.Schema({
  first_name: {
    type: String,
    required: true,
  },
  last_name: {
    type: String,
  },
  email: {
    type: String,
    required: true,
    unique: true,
  },
  job_title: {
    type: String,
  },
  gender: {
    type: String,
  },
});

const User = mongo.model("user", userSchema);
mongo
  .connect("mongodb://127.0.0.1:27017/PROJECT-01")
  .then(() => console.log("MongoDB Connected"))
  .catch(() => console.log("MongoDB error"));

app.get("/", (req, res) => {
  return res.json({
    res: "Radhe Radhe",
    project: "First Project Learning to use Rest APIs and Middlewares",
    routes: ["/api/users", "/users", "/api/users/:id", "/createUser"],
  });
});

app.get("/api/users", (req, res) => {
  console.log(users);
  return res.json(users);
});

app.get("/users", (req, res) => {
  const html = `<ul>${users
    .map((user) => `<li>${user.first_name}</li>`)
    .join("")}</ul>`;
  return res.send(html);
});

app
  .route("/api/users/:id")
  .get((req, res) => {
    const id = req.params.id;
    const user = users.find((user) => user.id == id);
    return res.send(user);
  })
  .delete((req, res) => {
    const id = req.params.id;
    const userIndex = users.findIndex((user) => user.id == id);

    if (userIndex !== -1) {
      const updatedUserData = users.filter((user) => user.id != id);

      // Write the updated data to MOCK_DATA.json
      fs.writeFile(
        "./MOCK_DATA.json",
        JSON.stringify(updatedUserData),
        (err) => {
          if (err) {
            return res.status(500).json({ desc: "Error deleting user." });
          }

          return res.json({
            desc: "User deleted successfully",
          });
        }
      );
    } else {
      // If user not found, send the 404 response
      return res.status(404).json({
        desc: "User not found",
      });
    }
  });

app.post("/createUser", async (req, res) => {
  // let largest = 0;
  // for (const element of users) {
  //   if (element.id > largest) {
  //     largest = element.id;
  //   }
  // }
  // const body = req.body;
  // const result = await User.create(
  //   {
  //     first_name: body.first_name,
  //     last_name: body.last_name,
  //     email: body.email,
  //     gender: body.gender,
  //     job_title: body.job_title,
  //   },
  //   { timestamps: true }
  // );
  // console.log(`result: ${result}`);
  // return res.status(201).json({ msg: "User created" });
  try {
    const { first_name, last_name, email, gender, job_title } = req.body;
    console.log(req.body); // To see what data is being received

    if (!first_name || !email) {
      return res
        .status(400)
        .json({ error: "First name and email are required" });
    }

    // Create a new user using the request body
    const result = await User.create({
      first_name,
      last_name,
      email,
      gender,
      job_title,
    });

    return res
      .status(201)
      .json({ msg: "User created successfully", user: result });
  } catch (error) {
    console.error(error);
    return res.status(400).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Radhe Radhe.... Server Started on port: ${PORT}`);
});
