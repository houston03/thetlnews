import React, { useState } from 'react';
import axios from 'axios';

const RegisterForm = ({ onSwitchToLogin }) => {
  const [email, setEmail] = useState('');
  const [nickname, setNickname] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    try {
      const response = await axios.post('http://localhost:8000/auth/register', {
        email,
        nickname,
        password,
        confirm_password: confirmPassword,
      });
      alert('Registration successful');
    } catch (error) {
      console.error('Error:', error.response || error.message);
      alert(`Registration failed: ${error.response?.data?.detail || 'Unknown error'}`);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>
      <div>
        <label>Email:</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      </div>
      <div>
        <label>Nickname:</label>
        <input type="text" value={nickname} onChange={(e) => setNickname(e.target.value)} required />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      </div>
      <div>
        <label>Confirm Password:</label>
        <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
      </div>
      <button type="submit">Register</button>
      <button type="button" onClick={onSwitchToLogin}>Already registered?</button>
    </form>
  );
};

export default RegisterForm;
