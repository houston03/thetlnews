import React from 'react';

function Header() {
  return (
    <header>
      <h1>Мое приложение</h1>
      <nav>
        <ul>
          <li><a href="/">Главная</a></li>
          <li><a href="/about">О нас</a></li>
          {/* Добавьте другие ссылки здесь */}
        </ul>
      </nav>
    </header>
  );
}

export default Header;