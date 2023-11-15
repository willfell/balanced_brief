import React, { useState } from 'react';
import './style.css';
function NewsForm() {
  const [newsChecked, setNewsChecked] = useState(false);
  const [generalNewsChecked, setGeneralNewsChecked] = useState(false);
  const [worldNewsChecked, setWorldNewsChecked] = useState(false);
  // Add states for other checkboxes similarly

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [age, setAge] = useState('');
  const [occupation, setOccupation] = useState('')
  const [email, setEmail] = useState('');

  const handleNewsChange = (event) => {
    const isChecked = event.target.checked;
    setNewsChecked(isChecked);
    setGeneralNewsChecked(isChecked);  // Assuming child checkboxes should match the parent
    setWorldNewsChecked(isChecked);
    // Add logic for other child checkboxes if needed
  };

  // New handlers for text inputs
  const handleFirstNameChange = (event) => setFirstName(event.target.value);
  const handleLastNameChange = (event) => setLastName(event.target.value);
  const handleAgeChange = (event) => setAge(event.target.value);
  const handleOccupationChange = (event) => setOccupation(event.target.value)
  const handleEmailChange = (event) => setEmail(event.target.value);

  // Update handleSubmit
  const handleSubmit = (event) => {
    event.preventDefault();
    // Add logic to handle form submission, including new fields
  };

  return (
    <div className="container mt-4">
      <form id="newsForm" onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-check-label">
            <input type="checkbox" className="form-check-input" id="news" value="news"
                   checked={newsChecked} onChange={handleNewsChange} /> News
          </label>
          <div className="form-check ml-3 indented-checkbox">
            <label className="form-check-label">
              <input type="checkbox" className="form-check-input news" value="General News" checked={generalNewsChecked} onChange={() => setGeneralNewsChecked(!generalNewsChecked)} /> General News
            </label>
          </div>
          <div className="form-check ml-3 indented-checkbox">
            <label className="form-check-label">
              <input type="checkbox" className="form-check-input news" value="World News" checked={worldNewsChecked} onChange={() => setWorldNewsChecked(!worldNewsChecked)} /> World News
            </label>
          </div>
          {/* Repeat for other checkboxes, using their respective states and handlers */}
        </div>
        {/* Other form sections */}
        <div className="form-group">
          <label htmlFor="first-name">First Name:</label>
          <input type="text" className="form-control" id="first-name" value={firstName} onChange={handleFirstNameChange} required />
        </div>

        <div className="form-group">
          <label htmlFor="last-name">Last Name:</label>
          <input type="text" className="form-control" id="last-name" value={lastName} onChange={handleLastNameChange} required />
        </div>

        <div className="form-group">
          <label htmlFor="age">Age:</label>
          <input type="text" className="form-control" id="age" value={age} onChange={handleAgeChange} required />
        </div>

        <div className="form-group">
          <label htmlFor="occupation">Occupation:</label>
          <input type="text" className="form-control" id="occupation" value={age} onChange={handleOccupationChange} required />
        </div>


        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input type="text" className="form-control" id="email" value={email} onChange={handleEmailChange} required />
        </div>
       
        <button type="submit" className="btn btn-primary">Submit</button>
      </form>
    </div>
  );
}

export default NewsForm;
