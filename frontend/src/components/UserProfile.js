import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UserProfile = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Замените на ваш API для получения данных пользователя
    const fetchUserProfile = async () => {
      try {
        const response = await axios.get('http://localhost:8000/auth/profile');
        setUser(response.data);
      } catch (error) {
        alert('Failed to fetch user profile');
      }
    };

    fetchUserProfile();
  }, []);

  if (!user) {
    return <div>Loading...</div>;
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
