// The exported code uses Tailwind CSS. Install Tailwind CSS in your dev environment to ensure all styles work.
import React, { type FC } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { UnitProvider } from './context/UnitContext';
import { UserProvider } from './context/UserContext';
import HomePage from './pages/HomePage';
import SettingsPage from './pages/SettingsPage';

const App: FC = () => {
  return (
    <ThemeProvider>
      <UnitProvider>
        <UserProvider>
          <Router>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </Router>
        </UserProvider>
      </UnitProvider>
    </ThemeProvider>
  );
};

export default App;
