interface YouTubeVideosProps {
  location: string;
  darkMode: boolean;
}

const YouTubeVideos = ({ location, darkMode }: YouTubeVideosProps) => {
  return (
    <section className="mt-8 space-y-8">
      <h2 className="text-2xl font-semibold">
        Weather News & City Highlights
      </h2>
      <div
        className={`rounded-xl shadow-lg overflow-hidden ${darkMode ? "bg-gray-800" : "bg-white"} p-6`}
      >
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="aspect-video rounded-lg overflow-hidden bg-gray-200">
            <iframe
              className="w-full h-full"
              src={`https://www.youtube.com/embed?search=weather+forecast+${location}&type=video`}
              title={`Weather in ${location}`}
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
          <div className="aspect-video rounded-lg overflow-hidden bg-gray-200">
            <iframe
              className="w-full h-full"
              src={`https://www.youtube.com/embed?search=${location}+city+tour&type=video`}
              title={`${location} City Highlights`}
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
          <div className="aspect-video rounded-lg overflow-hidden bg-gray-200">
            <iframe
              className="w-full h-full"
              src={`https://www.youtube.com/embed?search=${location}+travel+guide&type=video`}
              title={`${location} Travel Guide`}
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
        </div>
      </div>
    </section>
  );
};

export default YouTubeVideos;
