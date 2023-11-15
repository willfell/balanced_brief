import React, { useState } from 'react';
import './style.css';
import bbImage from '../assets/bb.png'; 
import SignUpForm from './NewsForm.js'
// Import Bootstrap CSS in the entry file (index.js or App.js) instead of here
// import 'bootstrap/dist/css/bootstrap.min.css'; 

function LandingPage() {
  const [email, setEmail] = useState('');
  const [showFullForm, setShowFullForm] = useState(false);

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handleSubscribeClick = () => {
    setShowFullForm(true);
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    // Process the form submission, e.g., send to the server
  };
  const [isClosing, setIsClosing] = useState(false);

  const handleCloseForm = () => {
    setIsClosing(true);
    setTimeout(() => {
      setShowFullForm(false);
      setIsClosing(false);
    }, 500); // Match this duration with your animation duration
  };
      
  return (
    <div className="container landing-page-container">
    <img src={bbImage} className="small-image" alt="Description" /> {/* Display the image */}
      <p className="lead">Sign up for the Balanced Brief or else.</p>
      
      {!showFullForm ? (
        <div className="initial-email-input input-group mb-3">
          <input type="email" className="form-control" value={email} onChange={handleEmailChange} placeholder="Enter Email" />
          <div className="input-group-append">
            <button className="btn btn-primary" type="button" onClick={handleSubscribeClick}>SUBSCRIBE FOR FREE</button>
          </div>
        </div>
      ) : (
        
<form onSubmit={handleFormSubmit} className={`mt-4 animated-form ${isClosing ? 'slide-up-form' : ''}`}>
  <div className="close-form" onClick={handleCloseForm}>X</div>
  <SignUpForm />
</form>
      )}
    </div>
  );
}

export default LandingPage;
