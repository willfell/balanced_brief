import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignUpPage from './components/LandingPage.js';
import VerifyUser from './components/VerifyUser.js'; 
import UnsubscribeUser from './components/UnsubscribeUser.js'; 
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<SignUpPage />} />
        <Route path="/user/verify" element={<VerifyUser />} />
        <Route path="/user/unsubscribe" element={<UnsubscribeUser />} />
      </Routes>
    </Router>
  );
}

export default App;
