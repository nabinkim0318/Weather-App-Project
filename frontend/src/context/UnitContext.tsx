import React, { createContext, useContext, useState, useEffect } from 'react';

type TemperatureUnit = 'celsius' | 'fahrenheit';

interface UnitContextType {
  unit: TemperatureUnit;
  toggleUnit: () => void;
  convertTemperature: (value: number, targetUnit?: TemperatureUnit) => number;
}

const UnitContext = createContext<UnitContextType | undefined>(undefined);

export const useUnit = () => {
  const context = useContext(UnitContext);
  if (context === undefined) {
    throw new Error('useUnit must be used within a UnitProvider');
  }
  return context;
};

interface UnitProviderProps {
  children: React.ReactNode;
}

export const UnitProvider = ({ children }: UnitProviderProps) => {
  const [unit, setUnit] = useState<TemperatureUnit>(() => {
    // 로컬 스토리지에서 단위 설정을 불러옴
    const savedUnit = localStorage.getItem('temperatureUnit');
    return (savedUnit as TemperatureUnit) || 'celsius';
  });

  useEffect(() => {
    // 단위 변경 시 로컬 스토리지에 저장
    localStorage.setItem('temperatureUnit', unit);
  }, [unit]);

  const toggleUnit = () => {
    setUnit(unit === 'celsius' ? 'fahrenheit' : 'celsius');
  };

  const convertTemperature = (value: number, targetUnit?: TemperatureUnit) => {
    const convertTo = targetUnit || unit;
    if (convertTo === 'celsius') {
      return Math.round((value - 32) * 5 / 9);
    } else {
      return Math.round((value * 9 / 5) + 32);
    }
  };

  return (
    <UnitContext.Provider value={{ unit, toggleUnit, convertTemperature }}>
      {children}
    </UnitContext.Provider>
  );
};

export default UnitProvider;
