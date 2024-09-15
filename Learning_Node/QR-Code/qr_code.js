// Take Input from user
import inquirer from "inquirer";
import qr from 'qr-image';
import fs from 'fs';

inquirer
  .prompt([
    {
      message: "Type in your URL: ",
      name: "URL",
    },
  ])
  .then((answer) => {
    console.log(answer);
    const url = answer.URL;
    var qr_img = qr.image(url);
    qr_img.pipe(fs.createWriteStream('qr_img.png'));
  })
  .catch((err) => {
    if (err.isTtyError) {
      console.log(`Promt couldn't be rendered in the current environment`);
    } else {
      console.log("Something went wrong");
    }
  });
