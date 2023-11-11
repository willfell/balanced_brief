// script.js

// When a parent checkbox is clicked, all children checkboxes are checked/unchecked
function toggleChildren(event) {
    let children = document.querySelectorAll('.' + event.target.id);
    children.forEach(child => {
        child.checked = event.target.checked;
    });
}

function isValidEmail(email) {
    var emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return emailRegex.test(email);
}

// Gather data and send a POST request
function submitForm() {

    let email = document.getElementById('email').value;

    // Validate email
    if (!isValidEmail(email)) {
        alert('Please enter a valid email address.');
        return; // Stop the function execution
    }

    let formData = {
        email: document.getElementById('email').value,
        first_name: document.getElementById('first-name').value,
        last_name: document.getElementById('last-name').value,
        age: parseInt(document.getElementById('age').value, 10),
        selections: []  // Array to hold all non-category selections
    };

    // Get all checked checkboxes
    document.querySelectorAll('input[type=checkbox]:checked').forEach(checkbox => {
        // Check if the parent element of the checkbox has the class 'category'
        if (!checkbox.closest('.category')) {
            // Add the value of each checked item to the selections array
            formData.selections.push(checkbox.value);
        }
    });

    // POST request to the server
    fetch('http://localhost:3000/user/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch((error) => {
            console.error('Error:', error);
        });
}
