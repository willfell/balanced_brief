import React, { useState } from 'react';
import './page.css';
import bbImage from '../assets/bb.png';
import SignUpForm from './NewsForm.js'


// Import Bootstrap CSS in the entry file (index.js or App.js) instead of here
// import 'bootstrap/dist/css/bootstrap.min.css'; 

function LandingPage() {
  const [email, setEmail] = useState('');
  const [showFullForm, setShowFullForm] = useState(false);

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

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSubscribeClick();
    }
  };  

  const handleSubscribeClick = () => {
    if (validateEmail(email)) {
      setShowFullForm(true);
      document.body.classList.add('full-page-form-active'); // Disable scrolling on the body
    } else {
      alert('Please enter a valid email address.'); // Show pop-up error message
    }
  };
  
  const handleFormSubmit = (event) => {
    console.log("You're in the wrong function")
    event.preventDefault();
    // Process the form submission, e.g., send to the server
  };
  const [isClosing, setIsClosing] = useState(false);

  const handleCloseForm = () => {
    setIsClosing(true);
    setTimeout(() => {
      setShowFullForm(false);
      setIsClosing(false);
      document.body.classList.remove('full-page-form-active'); // Enable scrolling on the body
    }, 500); // Match this duration with your animation duration
  };

  return (

    <div className="container landing-page-container">
      <div className="sign-up-section">
        <img src={bbImage} className="small-image" alt="Description" />
        <h1 className="balanced-brief-text">Balanced Brief</h1>
        <p className="lead-top">Sign up free today.</p>
        <p className="lead-below">Or else.</p>
        <p className="summary">Welcome to the Balanced Brief, your one stop shot to get the articles YOU want succinctly summarized in 50 words or less. The news you desire without the fluff. All it takes is the time to smoke half a cigarette.</p>

        {!showFullForm ? (
          <div className="initial-email-input input-group mb-3">
            <input type="email" className="form-control" value={email} onChange={handleEmailChange} placeholder="Enter Email" onKeyDown={handleKeyDown}/>
            <div className="input-group-append">
              <button className="btn btn-primary" type="button" onClick={handleSubscribeClick}>SUBSCRIBE FOR FREE</button>
            </div>
          </div>
        ) : (
          <div className="full-page-form">
            <img src={bbImage} className="logo" alt="Description" />
              <div className="close-form" onClick={handleCloseForm}>X</div>
              <SignUpForm email={email}/>
          </div>
        )}
      </div>
    </div>
  );
}

export default LandingPage;
