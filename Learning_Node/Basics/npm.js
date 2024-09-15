// Learn to import node module

import superheroes from "superheroes";

const random = Math.ceil(Math.random() * 1824);
console.log(random);
const name = superheroes.at(random);

console.log(name);
