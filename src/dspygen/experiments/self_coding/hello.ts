/**
 * @module HelloWorld
 * @description A simple Hello World program demonstrating TypeScript best practices
 */

/**
 * Generates a greeting message
 * @param name - The name to greet (optional)
 * @returns A greeting string
 */
function generateGreeting(name: string = 'World'): string {
  return `Hello, ${name}!`;
}

/**
 * Main function to execute the program
 */
function main(): void {
  const greeting = generateGreeting();
  console.log(greeting);
}

// Execute the program
main();