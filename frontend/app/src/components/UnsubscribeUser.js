import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import './page.css';
import 'bootstrap/dist/css/bootstrap.min.css'; // Ensure Bootstrap CSS is imported

function UnsubscribeUser() {
    const location = useLocation();
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const searchParams = new URLSearchParams(location.search);
    const initialEmail = searchParams.get('email') || ''; // Default to empty string if no email in query

    const unsubscribeUser = async (email) => {
        if (!email) return;

        const url = 'https://7o7oz1sgn0.execute-api.us-west-1.amazonaws.com/Prod/user/unsubscribe';
        const requestOptions = {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        };

        try {
            const response = await fetch(url, requestOptions);
            if (!response.ok) {
                const errorData = await response.json();
                const errorMessage = errorData.message || response.statusText;
                throw new Error(errorMessage);
                }
                const data = await response.json();
                console.log('Successfully Unsubscribed', data);
                setSuccessMessage('Successfully Unsubscribed!'); // Set success message
                setErrorMessage(''); // Clear any previous error messages
            } catch (error) {
                console.error('There was an error unsubscribing the user:', error);
                setErrorMessage('Error unsubscribing user: ' + error.message); // Set error message from the response
                setSuccessMessage(''); // Clear any previous success messages
            }
        };
        
    useEffect(() => {
        if (initialEmail) {
            unsubscribeUser(initialEmail);
        }
    }, [initialEmail]);


    // useEffect(() => {
    //     const searchParams = new URLSearchParams(location.search);
    //     const email = searchParams.get('email');
    //     unsubscribeUser(email);
    // }, [location]);

    // Validation schema for the form
    const validationSchema = Yup.object({
        email: Yup.string().email('Invalid email address').required('Required'),
    });

    return (
        <div className="container landing-page-container">
            <div className="sign-up-section">
                <img className="small-image" src="https://balanced-brief-frontend-assets.s3.us-west-1.amazonaws.com/bb.png" alt="Logo" />
                <h1 className="balanced-brief-text">Balanced Brief</h1>

                {/* Formik Form */}
                <Formik
                    initialValues={{ email: initialEmail }}
                    validationSchema={validationSchema}
                    onSubmit={(values, { setSubmitting }) => {
                        unsubscribeUser(values.email);
                        setSubmitting(false);
                    }}
                >
                    {({ isSubmitting, errors, touched }) => (
                        <Form>
                            <Field type="email" name="email" placeholder="Email" className={`form-control ${errors.email && touched.email ? 'is-invalid' : ''}`} />
                            <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
                                Unsubscribe
                            </button>
                            {errors.email && touched.email ? <div className="invalid-feedback">{errors.email}</div> : null}
                        </Form>
                    )}
                </Formik>

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

export default UnsubscribeUser;
