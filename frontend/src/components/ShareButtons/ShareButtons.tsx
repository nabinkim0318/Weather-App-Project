interface ShareButtonsProps {
  location: string;
  temperature: number;
  condition: string;
  unit: 'celsius' | 'fahrenheit';
}

const ShareButtons = ({
  location,
  temperature,
  condition,
  unit,
}: ShareButtonsProps) => {
  const handleCopyLink = () => {
    const url = `https://weather.app/share/${location}`;
    navigator.clipboard.writeText(url);
    alert("Link copied to clipboard!");
  };

  const handleShareTwitter = () => {
    const url = `https://twitter.com/intent/tweet?text=Check out the weather in ${location}: ${temperature}° ${unit === "celsius" ? "C" : "F"}, ${condition}&url=https://weather.app/share/${location}`;
    window.open(url, "_blank");
  };

  const handleShareFacebook = () => {
    const url = `https://www.facebook.com/sharer/sharer.php?u=https://weather.app/share/${location}`;
    window.open(url, "_blank");
  };

  return (
    <div className="flex items-center gap-4">
      <button
        onClick={handleCopyLink}
        className="flex items-center justify-center w-10 h-10 bg-blue-400 text-white rounded-lg hover:bg-blue-500 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
        title="Copy share link"
      >
        <i className="fas fa-link text-lg"></i>
      </button>
      <button
        onClick={handleShareTwitter}
        className="flex items-center justify-center w-10 h-10 bg-sky-400 text-white rounded-lg hover:bg-sky-500 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
        title="Share on Twitter"
      >
        <i className="fab fa-twitter text-lg"></i>
      </button>
      <button
        onClick={handleShareFacebook}
        className="flex items-center justify-center w-10 h-10 bg-indigo-400 text-white rounded-lg hover:bg-indigo-500 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
        title="Share on Facebook"
      >
        <i className="fab fa-facebook-f text-lg"></i>
      </button>
    </div>
  );
};

export default ShareButtons;
