import React from 'react';
import ReactDOM from 'react-dom';
import App from './App'; // Корневой компонент приложения

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root') // Точка привязки из public/index.html
);