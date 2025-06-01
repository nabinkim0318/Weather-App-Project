# Weather Dashboard

A full-stack weather application built with React and FastAPI that provides current weather, forecasts, and travel-related content.

## Features

- Multi-format location input (city names, ZIP codes, GPS coordinates, landmarks)
- Current weather conditions with detailed metrics
- 5-day weather forecast
- Hourly temperature charts
- GPS-based current location detection
- Weather history search with date ranges
- YouTube video integration (weather, restaurants, weekend activities)
- Interactive Google Maps
- Data export (JSON, CSV)
- Responsive design with dark/light themes
- Favorites system for locations

## Tech Stack

**Frontend:**
- React 18 with TypeScript
- Tailwind CSS
- ECharts for data visualization

**Backend:**
- FastAPI (Python)
- SQLAlchemy ORM
- PostgreSQL database

**APIs:**
- OpenWeatherMap API
- YouTube Data API v3
- Google Maps API

## Installation

### Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL 13+

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Edit `.env` file with your API keys:
```
OPENWEATHER_API_KEY=your_openweather_api_key
YOUTUBE_API_KEY=your_youtube_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
DATABASE_URL=postgresql://username:password@localhost/weather_db
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd my-app
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

## Usage

1. Open http://localhost:3000 in your browser
2. Enter a location using any of these formats:
   - City name: "New York", "Seoul"
   - ZIP code: "10001", "90210"
   - Coordinates: "37.5665,126.978"
   - Landmark: "Times Square"
3. Click "Search" or use "Current Location" for GPS detection
4. View current weather, forecasts, and related travel content

## API Endpoints

### Weather
- `GET /api/location/weather?user_input={location}` - Current weather
- `GET /api/weather/forecast?city={city}` - 5-day forecast
- `GET /api/weather/hourly?city={city}` - Hourly forecast

### Location
- `POST /api/location/search` - Search locations

### History
- `GET /api/weather-history/location/{location}` - Weather history

### Integrations
- `GET /api/integrations/youtube?city={city}` - Travel videos
- `GET /api/integrations/map?city={city}` - Maps

## Testing

Run backend tests:
```bash
cd backend
pytest tests/ -v
```

Run frontend tests:
```bash
cd my-app
npm test
```

## Project Structure

```
Weather-App-Project/
├── backend/
│   ├── app/
│   │   ├── api/              # API route handlers
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic
│   │   └── main.py          # FastAPI app
│   ├── tests/               # Test files
│   └── requirements.txt     # Python dependencies
├── my-app/
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   └── index.tsx        # Entry point
│   └── package.json         # Node dependencies
└── README.md
```

## Environment Variables

Create a `.env` file in the backend directory:

```
OPENWEATHER_API_KEY=your_api_key_here
YOUTUBE_API_KEY=your_api_key_here
GOOGLE_MAPS_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@localhost/weather_db
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is part of PM Accelerator 2025.

---

**Developer:** Nabin Kim | PM Accelerator 2025  
**Program:** Innovative Product Manager Training Program