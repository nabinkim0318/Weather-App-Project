interface UseMyLocationButtonProps {
  onUseMyLocation: () => void;
  className?: string;
}

const UseMyLocationButton = ({ onUseMyLocation, className = "" }: UseMyLocationButtonProps) => {
  return (
    <button
      onClick={onUseMyLocation}
      className={`flex items-center justify-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200 cursor-pointer whitespace-nowrap ${className}`}
    >
      <i className="fas fa-location-arrow mr-2"></i>
      My Location
    </button>
  );
};

export default UseMyLocationButton;
