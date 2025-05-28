import React, { FC } from 'react';

interface FooterProps {
  darkMode: boolean;
}

const Footer: FC<FooterProps> = ({ darkMode }) => {
  return (
    <footer
      className={`mt-12 py-6 ${
        darkMode ? "bg-gray-800 text-gray-300" : "bg-gray-100 text-gray-600"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 text-center">
        <p>Weather Dashboard &copy; 2025. All rights reserved.</p>
        <p className="text-sm mt-2">Last updated: May 27, 2025</p>
      </div>
    </footer>
  );
};

export default Footer; 