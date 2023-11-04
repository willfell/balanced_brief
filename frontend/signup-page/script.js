// script.js

// When a parent checkbox is clicked, all children checkboxes are checked/unchecked
function toggleChildren(event) {
    let children = document.querySelectorAll('.' + event.target.id);
    children.forEach(child => {
        child.checked = event.target.checked;
    });
}

// Gather data and send a POST request
function submitForm() {
    let formData = {
        news: [],
        email: document.getElementById('email').value
    };

    // Get all checked items
    document.querySelectorAll('input[type=checkbox]:checked').forEach(checkbox => {
        formData.news.push(checkbox.value);
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
