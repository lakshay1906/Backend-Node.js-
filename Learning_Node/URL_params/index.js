import express from "express";

const app = express();
const PORT = 3000;

app.use(express.json());

app.get("/", (req, res) => {
  console.log(`base route`);
  return res.send({ message: "Radhe Radhe" });
});

app.get("/:url", (req, res) => {
  console.log(`URL: ${req.params.url}`);
  res.send({ url: req.params.url });
});

app.get("/getId/:id", (req, res) => {
  console.log(`ID: ${req.params.id}`);
  res.send({ id: req.params.id });
});

app.listen(PORT, () =>
  console.log(`Server started at port http://localhost:${PORT} Radhe Radhe`)
);
