import React, { createContext, useContext, useState, useEffect } from 'react';

interface UserPreferences {
  favorites: string[];
  recentSearches: string[];
  defaultLocation?: string;
}

interface UserContextType {
  preferences: UserPreferences;
  addToFavorites: (location: string) => void;
  removeFromFavorites: (location: string) => void;
  addToRecentSearches: (location: string) => void;
  clearRecentSearches: () => void;
  setDefaultLocation: (location: string) => void;
}

const defaultPreferences: UserPreferences = {
  favorites: [],
  recentSearches: [],
};

const UserContext = createContext<UserContextType | undefined>(undefined);

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};

interface UserProviderProps {
  children: React.ReactNode;
}

export const UserProvider = ({ children }: UserProviderProps) => {
  const [preferences, setPreferences] = useState<UserPreferences>(() => {
    // 로컬 스토리지에서 사용자 설정을 불러옴
    const savedPreferences = localStorage.getItem('userPreferences');
    return savedPreferences ? JSON.parse(savedPreferences) : defaultPreferences;
  });

  useEffect(() => {
    // 설정 변경 시 로컬 스토리지에 저장
    localStorage.setItem('userPreferences', JSON.stringify(preferences));
  }, [preferences]);

  const addToFavorites = (location: string) => {
    if (!preferences.favorites.includes(location)) {
      setPreferences(prev => ({
        ...prev,
        favorites: [...prev.favorites, location],
      }));
    }
  };

  const removeFromFavorites = (location: string) => {
    setPreferences(prev => ({
      ...prev,
      favorites: prev.favorites.filter(fav => fav !== location),
    }));
  };

  const addToRecentSearches = (location: string) => {
    setPreferences(prev => {
      const newSearches = [
        location,
        ...prev.recentSearches.filter(search => search !== location),
      ].slice(0, 5); // 최근 5개 검색어만 유지
      return {
        ...prev,
        recentSearches: newSearches,
      };
    });
  };

  const clearRecentSearches = () => {
    setPreferences(prev => ({
      ...prev,
      recentSearches: [],
    }));
  };

  const setDefaultLocation = (location: string) => {
    setPreferences(prev => ({
      ...prev,
      defaultLocation: location,
    }));
  };

  return (
    <UserContext.Provider
      value={{
        preferences,
        addToFavorites,
        removeFromFavorites,
        addToRecentSearches,
        clearRecentSearches,
        setDefaultLocation,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};

export default UserProvider;
