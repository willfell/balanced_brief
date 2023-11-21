import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import './page.css';
import bbImage from '../assets/bb.png';

function VerifyUser() {
    const location = useLocation();

    // Define the verifyUser function inside your component
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
                // Handle response errors
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            const data = await response.json();
            // Handle success - you can set state to show a confirmation message, etc.
            console.log('Verification successful:', data);
        } catch (error) {
            // Handle or log error
            console.error('There was an error verifying the user:', error);
        }
    };

    useEffect(() => {
        // Extract the email parameter from the URL
        const searchParams = new URLSearchParams(location.search);
        const email = searchParams.get('email'); 

        // Call your API to verify the email
        verifyUser(email);
    }, [location]);

    return (
        <div className="container landing-page-container">
            <div className="sign-up-section">
                <img src={bbImage} className="small-image" alt="Balanced Brief" />
                <h1 className="balanced-brief-text">Balanced Brief</h1>
                {/* Add more content or UI elements as needed */}
            </div>
        </div>
    );
}

export default VerifyUser;
