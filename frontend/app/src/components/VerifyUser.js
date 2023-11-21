import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './page.css';
import bbImage from '../assets/bb.png';
import 'bootstrap/dist/css/bootstrap.min.css'; // Ensure Bootstrap CSS is imported

function VerifyUser() {
    const location = useLocation();
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const verifyUser = async (email) => {
        if (!email) return;

        const url = 'https://7o7oz1sgn0.execute-api.us-west-1.amazonaws.com/Prod/user/signup/verify';
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        };

        try {
            const response = await fetch(url, requestOptions);
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            const data = await response.json();
            console.log('Verification successful:', data);
            setSuccessMessage('Verification successful!'); // Set success message
            setErrorMessage(''); // Clear any previous error messages
        } catch (error) {
            console.error('There was an error verifying the user:', error);
            setErrorMessage('Error verifying user: ' + error.message); // Set error message
            setSuccessMessage(''); // Clear any previous success messages
        }
    };

    useEffect(() => {
        const searchParams = new URLSearchParams(location.search);
        const email = searchParams.get('email'); 
        verifyUser(email);
    }, [location]);

    return (
        <div className="container landing-page-container">
            <div className="sign-up-section">
                <img src={bbImage} className="small-image" alt="Balanced Brief" />
                <h1 className="balanced-brief-text">Balanced Brief</h1>
                {/* Display success or error message using Bootstrap alerts */}
                {successMessage && (
                    <div className="alert alert-success" role="alert">
                        {successMessage}
                    </div>
                )}
                {errorMessage && (
                    <div className="alert alert-danger" role="alert">
                        {errorMessage}
                    </div>
                )}
            </div>
        </div>
    );
}

export default VerifyUser;
