interface ExportButtonsProps {
  onExport: (format: 'csv' | 'json') => void;
}

const ExportButtons = ({ onExport }: ExportButtonsProps) => {
  return (
    <div className="flex items-center gap-4">
      <button
        onClick={() => onExport("csv")}
        className="flex items-center justify-center w-10 h-10 bg-emerald-400 text-white rounded-lg hover:bg-emerald-500 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
        title="Export as CSV"
      >
        <i className="fas fa-file-csv text-lg"></i>
      </button>
      <button
        onClick={() => onExport("json")}
        className="flex items-center justify-center w-10 h-10 bg-amber-400 text-white rounded-lg hover:bg-amber-500 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
        title="Export as JSON"
      >
        <i className="fas fa-file-code text-lg"></i>
      </button>
      <button
        onClick={() => window.print()}
        className="flex items-center justify-center w-10 h-10 bg-gray-400 text-white rounded-lg hover:bg-gray-500 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
        title="Print weather report"
      >
        <i className="fas fa-print text-lg"></i>
      </button>
    </div>
  );
};

export default ExportButtons;
