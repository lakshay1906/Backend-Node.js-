const express = require("express");
const { connectToMongoDB } = require("./connect");
const urlRoute = require("./Routes/url");
const app = express();
const PORT = 3000;

connectToMongoDB("mongodb://localhost:27017/short-url").then(() =>
  console.log("Mongodb connected")
);

app.use(express.json());

app.use("url", urlRoute);

app.listen(PORT, () =>
  console.log(`Radhe Radhe....Server Started at port: ${PORT}`)
);
