const COUNT_LIMIT = 3;

let message = "Hello from a sample JavaScript file!";

/**
 * Greets a user by their name.
 * 
 * This function takes a user's name as input and constructs a personalized
 * welcome message.
 * 
 * @param {string} name The name of the user to greet.
 * @returns {string} A personalized welcome message for the user.
 */
function greetUser(name) {
  return `Hello, ${name}! Welcome to the world of JavaScript.`;
}
let greeting = greetUser("User");

console.log(message);
console.log(greeting);

let sum = num1 + num2;
console.log(`The sum of ${num1} and ${num2} is: ${sum}`);

if (sum > 10) {
  console.log("The sum is greater than 10.");
} else {
  console.log("The sum is not greater than 10.");
}

console.log("Counting from 1 to 3:");
for (let i = 1; i <= COUNT_LIMIT; i++) {
  console.log(i);
}