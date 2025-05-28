import React, { type FC } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import { useUnit } from '../context/UnitContext';
import { useUser } from '../context/UserContext';
import UnitToggle from '../components/UnitToggle';
import ThemeToggle from '../components/ThemeToggle';

const SettingsPage: FC = () => {
  const navigate = useNavigate();
  const { darkMode, toggleTheme } = useTheme();
  const { unit, toggleUnit } = useUnit();
  const {
    preferences,
    clearRecentSearches,
    setDefaultLocation,
  } = useUser();

  const handleDefaultLocationChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setDefaultLocation(e.target.value);
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-800'}`}>
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">설정</h1>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors"
          >
            홈으로 돌아가기
          </button>
        </div>

        <div className="space-y-8">
          {/* 앱 설정 섹션 */}
          <section className={`p-6 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-lg`}>
            <h2 className="text-xl font-semibold mb-6">앱 설정</h2>
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium">다크 모드</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    앱의 테마를 변경합니다
                  </p>
                </div>
                <ThemeToggle darkMode={darkMode} onToggle={toggleTheme} />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium">온도 단위</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    온도 표시 단위를 변경합니다
                  </p>
                </div>
                <UnitToggle unit={unit} onToggle={toggleUnit} />
              </div>
            </div>
          </section>

          {/* 위치 설정 섹션 */}
          <section className={`p-6 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-lg`}>
            <h2 className="text-xl font-semibold mb-6">위치 설정</h2>
            <div className="space-y-6">
              <div>
                <label htmlFor="defaultLocation" className="block font-medium mb-2">
                  기본 위치
                </label>
                <select
                  id="defaultLocation"
                  value={preferences.defaultLocation || ''}
                  onChange={handleDefaultLocationChange}
                  className={`w-full p-2 rounded-lg border ${
                    darkMode
                      ? 'bg-gray-700 border-gray-600'
                      : 'bg-white border-gray-300'
                  }`}
                >
                  <option value="">위치를 선택하세요</option>
                  {preferences.favorites.map((location) => (
                    <option key={location} value={location}>
                      {location}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <h3 className="font-medium mb-2">최근 검색 기록</h3>
                <div className="flex items-center justify-between">
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    저장된 검색 기록: {preferences.recentSearches.length}개
                  </p>
                  <button
                    onClick={clearRecentSearches}
                    className="px-4 py-2 text-sm font-medium text-red-500 hover:text-red-600 transition-colors"
                  >
                    검색 기록 삭제
                  </button>
                </div>
              </div>
            </div>
          </section>

          {/* 데이터 관리 섹션 */}
          <section className={`p-6 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-lg`}>
            <h2 className="text-xl font-semibold mb-6">데이터 관리</h2>
            <div className="space-y-4">
              <p className="text-sm text-gray-500 dark:text-gray-400">
                즐겨찾기 위치: {preferences.favorites.length}개
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                최근 검색: {preferences.recentSearches.length}개
              </p>
              <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                <button
                  onClick={() => {
                    // TODO: 데이터 내보내기 구현
                    alert('준비 중인 기능입니다.');
                  }}
                  className="px-4 py-2 text-sm font-medium text-blue-500 hover:text-blue-600 transition-colors"
                >
                  데이터 내보내기
                </button>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
