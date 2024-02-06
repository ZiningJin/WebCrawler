import React from 'react';
import axios from 'axios';
import { useState } from 'react';
import './pec.css';

const Pec = () => { 
  const [formData, setFormData] = useState({
    username:'',
    password:'',
    auth_code:'',
    start_date_str:'',
    end_date_str:''
  });

  const [sessionID, setSessionID] = useState('');
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');

  // login-ing
  const[logining, setLogining] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLogin = async () => {
    setError('');
    setLogining(true); // login-ing
    try {
        const response = await axios.post('http://localhost:5000/api/pec_login', {
            username: formData.username,
            password: formData.password
        });
        if (response.data.session_id) {
            setSessionID(response.data.session_id);
        } else {
            setError('Login failed. Please check your credentials.');
        }
    } catch (err) {
        setError('An error occurred during login.');
        console.error(err);
        setLogining(false); // login-ing
    }
  };

  const handleProcess = async () => {
    setError('');
    setProcessing(true);
    try {
        const response = await axios.post('http://localhost:5000/api/pec_process', {
            session_id: sessionID,
            auth_code: formData.auth_code,
            start_date_str: formData.start_date_str,
            end_date_str: formData.end_date_str
        }, {
            responseType: 'blob', // Important for handling the binary data of the CSV
        });
        const url = window.URL.createObjectURL(new Blob([response.data])); // Create a URL for the blob
        const link = document.createElement('a'); // Create a temporary link to trigger the download
        link.href = url;
        link.setAttribute('download', 'pec_data.csv'); // or any other filename
        document.body.appendChild(link);
        link.click();            
        link.parentNode.removeChild(link); // Clean up
        window.URL.revokeObjectURL(url); // Free up memory
        setProcessing(false);
    } catch (err) {
        setError('An error occurred during processing.');
        console.error(err);
        setProcessing(false);
    }
 };


  return (
    <section id="pec">
      <div className="container pec__container">
        <div className="card">
          <h3>Video You Must Watch</h3>
          {/* <iframe src='' allowFullScreen title="Intro Video"></iframe> */}
          <a href="" target='_ blank' rel="noopener noreferrer">Video</a>
        </div>

        <div className="card">
          {error && <p className="error">{error}</p >}
              {!sessionID ? (
                  <div>
                      <input
                          type="text"
                          name="username"
                          placeholder="Username"
                          value={formData.username}
                          onChange={handleChange}
                      />
                      <input
                          type="password"
                          name="password"
                          placeholder="Password"
                          value={formData.password}
                          onChange={handleChange}
                      />
                      {logining ? (
                          <p>login-ing…</p >
                      ) : (
                        <button onClick={handleLogin}>Login</button>
                      )}
                  </div>
              ) : (
                  <div>
                      <input
                          type="text"
                          name="auth_code"
                          placeholder="Authentication Code"
                          value={formData.auth_code}
                          onChange={handleChange}
                      />
                      <input
                          type="text"
                          name="start_date_str"
                          placeholder="Start Date: 30-Jan-2024"
                          value={formData.start_date_str}
                          onChange={handleChange}
                      />
                      <input
                          type="text"
                          name="end_date_str"
                          placeholder="End Date: 28-Sep-2030"
                          value={formData.end_date_str}
                          onChange={handleChange}
                      />
                      {processing ? (
                          <p>Processing…</p >
                      ) : (
                          <button onClick={handleProcess}>Process</button>
                      )}
                  </div>
              )}

        </div>
      </div>
    </section>
  )
}

export default Pec
