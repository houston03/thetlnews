import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UserProfile = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const token = localStorage.getItem('token'); // Проверяем токен
        if (!token) {
          alert('Unauthorized access');
          window.location.href = '/auth'; // Редирект на страницу авторизации
          return;
        }

        const response = await axios.get('http://localhost:8000/auth/profile', {
          headers: { Authorization: `Bearer ${token}` }, // Отправляем токен
        });
        setUser(response.data); // Устанавливаем данные пользователя
      } catch (error) {
        alert('Failed to fetch user profile'); // Обработка ошибок
        console.error(error);
      }
    };

    fetchUserProfile(); // Вызываем функцию
  }, []); // Зависимость пустая — эффект выполняется только при монтировании компонента

  if (!user) {
    return <div>Loading...</div>; // Показ загрузки, пока данные не загружены
  }

  return (
    <div>
      <h2>User Profile</h2>
      <p>Email: {user.email}</p>
      <p>Nickname: {user.nickname}</p>
      <p>Registered At: {new Date(user.created_at).toLocaleString()}</p>
      <p>Role: {user.is_admin ? 'Admin' : 'User'}</p>
    </div>
  );
};

export default UserProfile;
