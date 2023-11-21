import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignUpPage from './components/LandingPage.js';
import VerifyUser from './components/VerifyUser.js'; // Import your verification component
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<SignUpPage />} />
        {/* Define other routes here */}
        <Route path="/user/verify" element={<VerifyUser />} />
      </Routes>
    </Router>
  );
}

export default App;
