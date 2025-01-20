import React, { useState } from 'react';
import axios from 'axios';

const LoginForm = ({ onSwitchToRegister }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Отправляем запрос на сервер
      const response = await axios.post('http://localhost:8000/auth/login', {
        email,
        password,
      });

      // Проверяем, что сервер вернул корректные данные
      const { token, user } = response.data;

      if (!token || !user) {
        throw new Error('Invalid response from server');
      }

      // Сохраняем токен в localStorage
      localStorage.setItem('token', token);

      alert('Login successful');

      // Перенаправление в зависимости от роли пользователя
      if (user.is_admin) {
        window.location.href = '/admin-panel';
      } else {
        window.location.href = '/profile';
      }
    } catch (error) {
      // Обработка ошибок
      alert('Login failed');
      console.error('Login error:', error.response?.data || error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      <div>
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit">Login</button>
      <button type="button" onClick={onSwitchToRegister}>
        Don't have an account?
      </button>
    </form>
  );
};

export default LoginForm;
