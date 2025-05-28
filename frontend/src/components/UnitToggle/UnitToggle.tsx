interface UnitToggleProps {
  unit: 'celsius' | 'fahrenheit';
  onToggle: () => void;
}

const UnitToggle = ({ unit, onToggle }: UnitToggleProps) => {
  return (
    <div className="flex items-center">
      <button
        onClick={onToggle}
        className={`relative inline-flex h-8 w-14 items-center rounded-full cursor-pointer whitespace-nowrap !rounded-button ${unit === "celsius" ? "bg-blue-500" : "bg-gray-400"}`}
      >
        <span
          className={`inline-block h-6 w-6 transform rounded-full bg-white transition ${unit === "celsius" ? "translate-x-7" : "translate-x-1"}`}
        />
      </button>
      <span className="ml-3 text-lg">
        °{unit === "celsius" ? "C" : "F"}
      </span>
    </div>
  );
};

export default UnitToggle;
