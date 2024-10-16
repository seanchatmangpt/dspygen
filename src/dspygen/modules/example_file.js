// example_file.js

// Function to fetch user details
function fetchUserDetails(userId) {
    const url = `https://api.example.com/users/${userId}`;
    const response = fetch(url).then(res => res.json());
    return response;
}

// Class representing a User
class User {
    constructor(id, name) {
        this.id = id;
        this.name = name;
    }

    greet() {
        return `Hello, my name is ${this.name}!`;
    }

    updateName(newName) {
        this.name = newName;
    }
}

// Function to log in a user
function loginUser(username, password) {
    if (username === "admin" && password === "1234") {
        console.log("Login successful!");
        return true;
    } else {
        console.log("Invalid credentials.");
        return false;
    }
}

// Helper function to display a message
function displayMessage(message) {
    console.log(message);
}
