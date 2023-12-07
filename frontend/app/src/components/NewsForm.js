import React, { useState } from 'react'; // Corrected import statement
import { Formik, Form, Field } from 'formik';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Checkbox from '@mui/material/Checkbox';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FormControlLabel from '@mui/material/FormControlLabel';
import { categoriesData } from './categoriesData';
import TextField from '@mui/material/TextField'; // If you want to use Material-UI TextField
import './page.css';
import 'bootstrap/dist/css/bootstrap.min.css'; // If installed via npm
import * as Yup from 'yup';

const validationSchema = Yup.object().shape({
    firstName: Yup.string().required('First Name is required'),
    lastName: Yup.string().required('Last Name is required'),
    dateOfBirth: Yup.date().required('Date of Birth is required'),
    email: Yup.string().email('Invalid email format').required('Email is required'),
    // Add any other fields you want to validate here
});


const CategoryForm = ({ email }) => {
    // Initial form state with new fields
    const initialValues = {
        firstName: '',
        lastName: '',
        dateOfBirth: '',
        email: email,
        ...categoriesData.categories.reduce((acc, category) => {
            category.subcategories.forEach(subcat => {
                acc[subcat] = false;
            });
            return acc;
        }, {})
    };
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submissionSuccess, setSubmissionSuccess] = useState(false);
    const [submissionError, setSubmissionError] = useState('');

    const handleSubmit = (values) => {
        setIsSubmitting(true);
        setSubmissionSuccess(false);
        setSubmissionError('');
        const newsSelections = categoriesData.categories.reduce((selected, category) => {
            category.subcategories.forEach(subcat => {
                if (values[subcat]) {
                    selected.push(subcat);
                }
            });
            return selected;
        }, []);

        // Preparing form data
        const formData = {
            newsSelected: newsSelections,
            firstName: values.firstName,
            lastName: values.lastName,
            dateOfBirth: values.dateOfBirth,
            email: values.email
        };

        // Send POST request
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
                setIsSubmitting(false);
                setSubmissionSuccess(true);
            })
            .catch((error) => {
                console.error('Error:', error);
                setIsSubmitting(false);
                setSubmissionError(error.message || 'An error occurred');
            });
    };

    return (
        <Formik initialValues={initialValues} onSubmit={handleSubmit} className="formik-form" validationSchema={validationSchema}>
            {({ values, errors, touched }) => (
                <Form>
                    {categoriesData.categories.map(category => (
                        <Accordion key={category.name}>
                            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                {category.name}
                            </AccordionSummary>
                            <AccordionDetails>
                                {category.subcategories.map(subcat => (
                                    <FormControlLabel
                                        key={subcat}
                                        control={<Field as={Checkbox} name={subcat} />}
                                        label={subcat}
                                    />
                                ))}
                            </AccordionDetails>
                        </Accordion>
                    ))}
                    <div className="form-section">
                        <div className="name-fields">
                            <Field as={TextField} name="firstName" label="First Name" className="first-name-field" />
                            {errors.firstName && touched.firstName && <div className="error">{errors.firstName}</div>}
                            <Field as={TextField} name="lastName" label="Last Name" className="last-name-field" />
                            {errors.lastName && touched.lastName && <div className="error">{errors.lastName}</div>}
                        </div>
                        <div className="date-email-fields">
                            <Field as={TextField} name="dateOfBirth" type="date" className="date-of-birth-field" />
                            {errors.dateOfBirth && touched.dateOfBirth && <div className="error">{errors.dateOfBirth}</div>}
                            <Field as={TextField} name="email" label="Email" type="email" className="email-text-box-field" />
                            {errors.email && touched.email && <div className="error">{errors.email}</div>}
                        </div>
                        <div className="submit-button">
                            <button
                                type="submit"
                                className={`submit-button-field ${isSubmitting ? 'submitting' : ''} ${submissionSuccess ? 'success' : ''}`}
                                disabled={isSubmitting}
                            >
                                {isSubmitting ? 'Submitting...' : 'Sign Up'}
                            </button>
                        </div>
                        {submissionError && <p className="error-message">{submissionError}</p>}
                        {submissionSuccess && <p className="success-message">Signup successful!</p>}

                    </div>
                </Form>
            )}
        </Formik>
    );
};
export default CategoryForm;
