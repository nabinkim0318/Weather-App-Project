import React, { FC } from 'react';
import { Link } from 'react-router-dom';
import LocationSearch from '../LocationSearch';
import UnitToggle from '../UnitToggle';
import ThemeToggle from '../ThemeToggle';
import ErrorMessage from '../ErrorMessage';

interface HeaderProps {
  darkMode: boolean;
  unit: 'celsius' | 'fahrenheit';
  onLocationSelect: (location: string) => void;
  onUseMyLocation: () => void;
  toggleUnit: () => void;
  toggleTheme: () => void;
  error?: string | null;
  locationError?: string | null;
}

const Header: FC<HeaderProps> = ({
  darkMode,
  unit,
  onLocationSelect,
  onUseMyLocation,
  toggleUnit,
  toggleTheme,
  error,
  locationError,
}) => {
  return (
    <header className="mb-8">
      <div className="flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center justify-between w-full md:w-auto">
          <h1 className="text-3xl font-bold mb-4 md:mb-0">
            <i className="fas fa-cloud-sun mr-2 text-blue-500"></i>
            Weather Dashboard
          </h1>
          <Link
            to="/settings"
            className="md:ml-4 text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-blue-500 dark:hover:text-blue-400"
          >
            <i className="fas fa-cog mr-1"></i>
            설정
          </Link>
        </div>
        <div className="flex items-center gap-4 w-full md:w-auto">
          <LocationSearch
            onLocationSelect={onLocationSelect}
            onUseMyLocation={onUseMyLocation}
            darkMode={darkMode}
          />
          <div className="flex items-center gap-8">
            <UnitToggle unit={unit} onToggle={toggleUnit} />
            <ThemeToggle darkMode={darkMode} onToggle={toggleTheme} />
          </div>
        </div>
      </div>
      {(error || locationError) && (
        <ErrorMessage message={error || locationError || ""} />
      )}
    </header>
  );
};

export default Header; 