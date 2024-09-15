// import express from "express";
// import users from "./MOCK_DATA.json";

const express = require("express");
const users = require("./MOCK_DATA.json");
const fs = require("fs");

const app = express();
const PORT = 1906;

app.use(express.urlencoded({ extended: false }));

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

app.post("/createUser", (req, res) => {
  console.log(req.body);
  let largest = 0;
  for (const element of users) {
    if (element.id > largest) {
      largest = element.id;
    }
  }
  users.push({ id: largest + 1, ...req.body });
  fs.writeFile("./MOCK_DATA.json", JSON.stringify(users), (err, data) => {
    if (err) {
      throw err;
    } else {
      //   res.sendStatus(201);
      return res.json({ status: "done", userId: largest + 1 });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Radhe Radhe.... Server Started on port: ${PORT}`);
});
