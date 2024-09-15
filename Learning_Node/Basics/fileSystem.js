const fs = require("fs");

const data = new Uint8Array(Buffer.from("SeetaRam"));

// To write some in a file.
// fs.writeFile("message.txt", data, (err) => {
//   if (err) {
//     throw err;
//   } else {
//     console.log("File Saved Successfully");
//   }
// });

// To Read a file
fs.readFile("./message.txt", "utf8", (err, data) => {
  if (err) {
    throw err;
  } else {
    console.log(data);
  }
});
