import React from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import AuthForm from './components/AuthForm';
import UserProfile from './components/UserProfile';

function App() {
  return (
        <Router>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/auth" element={<AuthForm />} />
            <Route path="/profile" element={<UserProfile />} />
          </Routes>
        </Router>
  );
}

export default App;