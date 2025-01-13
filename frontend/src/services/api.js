import axios from 'axios';

const API_URL = 'http://localhost:8000//api'; // URL вашего backend

export const getData = async () => {
  try {
    const response = await axios.get(`${API_URL}/data`);
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении данных:', error);
  }
};