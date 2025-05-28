interface ThemeToggleProps {
  darkMode: boolean;
  onToggle: () => void;
}

const ThemeToggle = ({ darkMode, onToggle }: ThemeToggleProps) => {
  return (
    <button
      onClick={onToggle}
      className={`p-3 rounded-full cursor-pointer whitespace-nowrap !rounded-button ${darkMode ? "bg-gray-700 text-yellow-400 hover:bg-gray-600" : "bg-gray-200 text-blue-900 hover:bg-gray-300"}`}
    >
      <i
        className={`fas ${darkMode ? "fa-sun text-xl" : "fa-moon text-xl"}`}
      ></i>
    </button>
  );
};

export default ThemeToggle;
