import React, { useState } from 'react';
import './page.css';

function NewsForm({ email: initialEmail }) {
  const [newsChecked, setNewsChecked] = useState(false);
  const [generalNewsChecked, setGeneralNewsChecked] = useState(false);
  const [worldNewsChecked, setWorldNewsChecked] = useState(false);
  const [financeChecked, setFinanceChecked] = useState(false);
  const [economicsChecked, setEconomicsChecked] = useState(false);
  const [techNewsChecked, setTechNewsChecked] = useState(false);
  const [gamingChecked, setGamingChecked] = useState(false);
  const [pcGamingChecked, setPCGamingChecked] = useState(false);
  const [programmingChecked, setProgrammingChecked] = useState(false);
  const [androidChecked, setAndroidChecked] = useState(false);
  const [appleChecked, setAppleChecked] = useState(false);
  const [scienceChecked, setScienceChecked] = useState(false);
  const [artificalChecked, setArtificialChecked] = useState(false);
  const [cateredChecked, setCateredChecked] = useState(false);
  const [conservativeChecked, setConservativeChecked] = useState(false);
  const [libertarianChecked, setLibertarianChecked] = useState(false);
  const [environmentChecked, setEnvironmentChecked] = useState(false);
  const [offBeatChecked, setOffBeatChecked] = useState(false);
  const [upliftingChecked, setUpliftingChecked] = useState(false);
  const [notTheOnionChecked, setNotTheOnionChecked] = useState(false);
  const [conspiracyChecked, setConspiracyChecked] = useState(false);
  const [sportsChecked, setSportsChecked] = useState(false);
  const [nflChecked, setNFLChecked] = useState(false);
  const [soccerChecked, setSoccerChecked] = useState(false);
  const [hockeyChecked, setHockeyChecked] = useState(false);
  const [nbaChecked, setNBAChecked] = useState(false);
  const [entertainmentChecked, setEntertainmentChecked] = useState(false);
  const [moviesChecked, setMoviesChecked] = useState(false);
  const [televisionChecked, setTelevisionChecked] = useState(false);


  // Add states for other checkboxes similarly

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [age, setAge] = useState('');
  const [email, setEmail] = useState(initialEmail);


  const handleEntertainmentChange = (event) => {
    const isChecked = event.target.checked;
    setEntertainmentChecked(isChecked);
    setMoviesChecked(isChecked);
    setTelevisionChecked(isChecked);
  };

  const handleMoviesChange = (event) => {
    setMoviesChecked(event.target.checked);
  };

  const handleTelevisionChange = (event) => {
    setTelevisionChecked(event.target.checked);
  };

  const handleSportsChange = (event) => {
    const isChecked = event.target.checked;
    setSportsChecked(isChecked);
    setNFLChecked(isChecked);
    setSoccerChecked(isChecked);
    setHockeyChecked(isChecked);
    setNBAChecked(isChecked);
  };

  const handleNFLChange = (event) => {
    setNFLChecked(event.target.checked);
  };

  const handleSoccerChange = (event) => {
    setSoccerChecked(event.target.checked);
  };

  const handleHockeyChange = (event) => {
    setHockeyChecked(event.target.checked);
  };

  const handleNBAChange = (event) => {
    setNBAChecked(event.target.checked);
  };


  const handleOffBeatChange = (event) => {
    const isChecked = event.target.checked;
    setOffBeatChecked(isChecked);
    setUpliftingChecked(isChecked);
    setNotTheOnionChecked(isChecked);
    setConspiracyChecked(isChecked);
  };

  const handleUpliftingChange = (event) => {
    setUpliftingChecked(event.target.checked);
  };

  const handleNotTheOnionChange = (event) => {
    setNotTheOnionChecked(event.target.checked);
  };

  const handleConspiracyChange = (event) => {
    setConspiracyChecked(event.target.checked);
  };


  const handleNewsChange = (event) => {
    const isChecked = event.target.checked;
    setNewsChecked(isChecked);
    setGeneralNewsChecked(isChecked);
    setWorldNewsChecked(isChecked);
  };

  const handleFinanceChange = (event) => {
    const isChecked = event.target.checked;
    setFinanceChecked(isChecked);
    setEconomicsChecked(isChecked);
  };

  const handleGeneralNewsChange = (event) => {
    setGeneralNewsChecked(event.target.checked);
  };

  const handleWorldNewsChange = (event) => {
    setWorldNewsChecked(event.target.checked);
  };

  const handleEconomicsChange = (event) => {
    setEconomicsChecked(event.target.checked);
  };

  const handleTechNewsChange = (event) => {
    const isChecked = event.target.checked;
    setTechNewsChecked(isChecked);
    setGamingChecked(isChecked);
    setPCGamingChecked(isChecked);
    setProgrammingChecked(isChecked);
    setAndroidChecked(isChecked);
    setAppleChecked(isChecked);
    setScienceChecked(isChecked);
    setArtificialChecked(isChecked);
  }

  const handleGamingChange = (event) => {
    setGamingChecked(event.target.checked);
  };

  const handlePCGamingChange = (event) => {
    setPCGamingChecked(event.target.checked);
  };

  const handleProgrammingChange = (event) => {
    setProgrammingChecked(event.target.checked);
  };

  const handleAndroidChange = (event) => {
    setAndroidChecked(event.target.checked);
  };

  const handleAppleChange = (event) => {
    setAppleChecked(event.target.checked);
  };
  const handleScienceChange = (event) => {
    setScienceChecked(event.target.checked);
  };
  const handleArtificialChange = (event) => {
    setArtificialChecked(event.target.checked);
  };

  const handleCateredChange = (event) => {
    const isChecked = event.target.checked;
    setCateredChecked(isChecked);
    setEnvironmentChecked(isChecked);
    setConservativeChecked(isChecked);
    setLibertarianChecked(isChecked);
  }

  const handleEnvironmentChange = (event) => {
    setEnvironmentChecked(event.target.checked);
  };

  const handleConservativeChange = (event) => {
    setConservativeChecked(event.target.checked);
  };

  const handleLibertarianChange = (event) => {
    setLibertarianChecked(event.target.checked);
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
    if (financeChecked) newsSelections.push('Finance');
    if (economicsChecked) newsSelections.push('Economics');
    if (techNewsChecked) newsSelections.push('Technology');
    if (gamingChecked) newsSelections.push('Gaming');
    if (pcGamingChecked) newsSelections.push('PC Gaming');
    if (programmingChecked) newsSelections.push('Programming');
    if (androidChecked) newsSelections.push('Android');
    if (appleChecked) newsSelections.push('Apple');
    if (scienceChecked) newsSelections.push('Science');
    if (artificalChecked) newsSelections.push('AI');
    if (conservativeChecked) newsSelections.push('Conservative News');
    if (libertarianChecked) newsSelections.push('Liberal News');
    if (environmentChecked) newsSelections.push('Environment');
    if (upliftingChecked) newsSelections.push('Uplifting News');
    if (notTheOnionChecked) newsSelections.push('Oddly Interesting News');
    if (conspiracyChecked) newsSelections.push('Conspiracy');
    if (sportsChecked) newsSelections.push('Sports');
    if (nflChecked) newsSelections.push('NFL');
    if (soccerChecked) newsSelections.push('Soccer');
    if (hockeyChecked) newsSelections.push('Hockey');
    if (nbaChecked) newsSelections.push('NBA');
    if (conspiracyChecked) newsSelections.push('Conspiracy');
    if (moviesChecked) newsSelections.push('Movies');
    if (televisionChecked) newsSelections.push('Television');


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
            <div className="category-group">
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

            <div className="category-group">
              <label className="form-check-label">
                <input type="checkbox" className="form-check-input" id="finance" value="Finance"
                  checked={financeChecked} onChange={handleFinanceChange} /> Finance
              </label>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="Economics" checked={economicsChecked} onChange={handleEconomicsChange} /> General News
                </label>
              </div></div>

            <div className="category-group">
              <label className="form-check-label">
                <input type="checkbox" className="form-check-input" id="tech-news" value="Tech News"
                  checked={techNewsChecked} onChange={handleTechNewsChange} /> Tech News
              </label>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="gaming" checked={gamingChecked} onChange={handleGamingChange} /> Gaming
                </label>
              </div>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="pc-gaming" checked={pcGamingChecked} onChange={handlePCGamingChange} /> PC Gaming
                </label>
              </div>

              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="programming" checked={programmingChecked} onChange={handleProgrammingChange} /> Programming
                </label>
              </div>

              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="Android" checked={androidChecked} onChange={handleAndroidChange} /> Android
                </label>
              </div>

              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="Apple" checked={appleChecked} onChange={handleAppleChange} /> Apple
                </label>
              </div>

              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="Science" checked={scienceChecked} onChange={handleScienceChange} /> Science
                </label>
              </div>

              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="Artificial" checked={artificalChecked} onChange={handleArtificialChange} /> AI News
                </label>
              </div></div>

            <div className="category-group">
              <label className="form-check-label">
                <input type="checkbox" className="form-check-input" id="catered-news" value="Catered"
                  checked={cateredChecked} onChange={handleCateredChange} /> Catered News
              </label>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="Environment" checked={environmentChecked} onChange={handleEnvironmentChange} /> Environment News
                </label>
              </div>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="Conservative" checked={conservativeChecked} onChange={handleConservativeChange} /> Conservative News
                </label>
              </div>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="Libertarian" checked={libertarianChecked} onChange={handleLibertarianChange} /> Libertarian News
                </label>
              </div></div>
            <div className="category-group">

              <label className="form-check-label">
                <input type="checkbox" className="form-check-input" id="off-beat" value="off-beat"
                  checked={offBeatChecked} onChange={handleOffBeatChange} /> Off Beat News
              </label>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="uplifting-news" checked={upliftingChecked} onChange={handleUpliftingChange} /> Uplifting News
                </label>
              </div>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="not-the-onion" checked={notTheOnionChecked} onChange={handleNotTheOnionChange} /> Oddly Interesting News
                </label>
              </div>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="conspiracy" checked={conspiracyChecked} onChange={handleConspiracyChange} /> Conspiracy News
                </label>
              </div></div>




            <div className="category-group">
              <label className="form-check-label">
                <input type="checkbox" className="form-check-input" id="sports" value="sports"
                  checked={sportsChecked} onChange={handleSportsChange} /> Sports
              </label>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="nfl" checked={nflChecked} onChange={handleNFLChange} /> NFL
                </label>
              </div>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="soccer" checked={soccerChecked} onChange={handleSoccerChange} /> Soccer
                </label>
              </div>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="hockey" checked={hockeyChecked} onChange={handleHockeyChange} /> Hockey
                </label>
              </div>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="nba" checked={nbaChecked} onChange={handleNBAChange} /> NBA
                </label>
              </div></div>

            <div className="category-group">
              <label className="form-check-label">
                <input type="checkbox" className="form-check-input" id="entertainment" value="entertainment"
                  checked={entertainmentChecked} onChange={handleEntertainmentChange} /> Entertainment
              </label>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="movies" checked={moviesChecked} onChange={handleMoviesChange} /> Movies
                </label>
              </div>
              <div className="form-check ml-3 indented-checkbox">
                <label className="form-check-label">
                  <input type="checkbox" className="form-check-input news" value="television" checked={televisionChecked} onChange={handleTelevisionChange} /> Television
                </label>
              </div></div>

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
