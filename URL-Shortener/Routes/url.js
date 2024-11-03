const express = require("express");
const { generateNewShortURL } = require("../Controllers/url");
const { allData } = require("../Controllers/sendingData");
const router = express.Router();

router.post("/", generateNewShortURL);
router.get("/all", allData);

module.exports = router;
