import React, { useState } from 'react';
import RegisterForm from './RegisterForm';
import LoginForm from './LoginForm';

const AuthForm = () => {
  const [isRegister, setIsRegister] = useState(true);

  const handleSwitchToLogin = () => setIsRegister(false);
  const handleSwitchToRegister = () => setIsRegister(true);

  return (
    <div>
      {isRegister ? (
        <RegisterForm onSwitchToLogin={handleSwitchToLogin} />
      ) : (
        <LoginForm onSwitchToRegister={handleSwitchToRegister} />
      )}
    </div>
  );
};

export default AuthForm;
