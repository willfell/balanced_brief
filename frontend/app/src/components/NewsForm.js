import React, { useState } from 'react';
import './page.css';

function NewsForm({ email: initialEmail }) {
  const [newsChecked, setNewsChecked] = useState(false);
  const [generalNewsChecked, setGeneralNewsChecked] = useState(false);
  const [worldNewsChecked, setWorldNewsChecked] = useState(false);
  // Add states for other checkboxes similarly

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [age, setAge] = useState('');
  const [email, setEmail] = useState(initialEmail);

  const handleNewsChange = (event) => {
    const isChecked = event.target.checked;
    setNewsChecked(isChecked);
    setGeneralNewsChecked(isChecked);
    setWorldNewsChecked(isChecked);
  };

  const handleGeneralNewsChange = (event) => {
    setGeneralNewsChecked(event.target.checked);
  };

  const handleWorldNewsChange = (event) => {
    setWorldNewsChecked(event.target.checked);
  };


  // New handlers for text inputs
  const handleFirstNameChange = (event) => setFirstName(event.target.value);
  const handleLastNameChange = (event) => setLastName(event.target.value);
  const handleAgeChange = (event) => {
    const value = event.target.value;
    // Allow only numeric input
    if (!isNaN(value) && !value.includes('.')) {
      setAge(value);
    }
  };


  const [emailError, setEmailError] = useState('');

  const validateEmail = (email) => {
    const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return regex.test(email);
  };

  const handleEmailChange = (event) => {
    const emailInput = event.target.value;
    setEmail(emailInput);

    // Validate email and update the emailError state
    if (validateEmail(emailInput)) {
      setEmailError('');
    } else {
      setEmailError('Invalid email format');
    }
  };

  const [submitStatus, setSubmitStatus] = useState({
    isLoading: false,
    successMessage: '',
    errorMessage: '',
  });

  const clearErrorMessage = () => {
    setSubmitStatus({ ...submitStatus, errorMessage: '' });
  };
  

  // Update handleSubmit
  const handleSubmit = (event) => {
    event.preventDefault();
    setSubmitStatus({ ...submitStatus, isLoading: true });

    
    // Prepare the data
    const numericAge = parseInt(age) || 0;  // Fallback to 0 if age is not a valid number
    if (!validateEmail(email)) {
      console.error('Invalid email address');
      return; // Stop the form submission
    }  
    const newsSelections = [];
    if (generalNewsChecked) newsSelections.push('General News');
    if (worldNewsChecked) newsSelections.push('World News');
    if (newsChecked) newsSelections.push('News');
    // Add other news types as necessary
  
    const formData = {
      newsSelected: newsSelections,
      firstName: firstName,
      lastName: lastName,
      age: numericAge,
      email: email
    };
  
    // Send POST request
    /* fetch('http://127.0.0.1:3000/user/signup', { */
    fetch('https://7o7oz1sgn0.execute-api.us-west-1.amazonaws.com/Prod/user/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(err => {
          throw new Error(err.message || 'Server responded with an error');
        });
      }
      return response.json();
    })
    .then(data => {
      console.log('Success:', data);
      setSubmitStatus({ isLoading: false, successMessage: 'Email submitted sucessfully. A verification email has been sent.', errorMessage: '' });
    })
    .catch((error) => {
      console.error('Error:', error);
      setSubmitStatus({ isLoading: false, successMessage: '', errorMessage: error.message });
    });
  };
  
  return (
    <div className="container mt-4">
      <form id="newsForm" onSubmit={handleSubmit}>
        <div className="checkbox-grid">
          <div className="form-group">
            <label className="form-check-label">
              <input type="checkbox" className="form-check-input" id="news" value="news"
                checked={newsChecked} onChange={handleNewsChange} /> News
            </label>
            <div className="form-check ml-3 indented-checkbox">
              <label className="form-check-label">
                <input type="checkbox" className="form-check-input news" value="General News" checked={generalNewsChecked} onChange={handleGeneralNewsChange} /> General News
              </label>
            </div>
            <div className="form-check ml-3 indented-checkbox">
              <label className="form-check-label">
                <input type="checkbox" className="form-check-input news" value="World News" checked={worldNewsChecked} onChange={handleWorldNewsChange} /> World News
              </label>
            </div>
          </div>
          {/* Repeat for other checkboxes, using their respective states and handlers */}
        </div>
        {/* Other form sections */}
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="first-name">First Name:</label>
            <input type="text" className="form-control" id="first-name" placeholder="First Name" value={firstName} onChange={handleFirstNameChange} required />
          </div>

          <div className="form-group">
            <label htmlFor="last-name">Last Name:</label>
            <input type="text" className="form-control" id="last-name" placeholder="Last Name" value={lastName} onChange={handleLastNameChange} required />
          </div>
        </div>
        <div className="form-group">
          <label htmlFor="age">Age:</label>
          <input type="text" className="form-control" id="age" placeholder="Age" value={age} onChange={handleAgeChange} required />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input type="text" className="form-control" id="email" placeholder="Email" value={email} onChange={handleEmailChange} required />
          {emailError && <div className="error-message">{emailError}</div>}
        </div>

        <div className="form-group">
  <button type="submit" className="btn btn-primary">
    {submitStatus.isLoading ? 'Submitting...' : 'Submit'}
  </button>
</div>
        {submitStatus.successMessage && <div className="alert alert-success">{submitStatus.successMessage}</div>}
        {submitStatus.errorMessage && <div className="alert alert-danger">{submitStatus.errorMessage}</div>}
      </form>
    </div>
  );
}

export default NewsForm;
