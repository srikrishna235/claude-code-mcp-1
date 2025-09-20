console.log("Hello from JavaScript!");
console.log("Current date:", new Date().toISOString());
console.log("Node version:", process.version);

const numbers = [1, 2, 3, 4, 5];
const sum = numbers.reduce((a, b) => a + b, 0);
console.log("Sum of", numbers, "is:", sum);