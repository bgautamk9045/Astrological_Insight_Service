# Astrological Insight Generator
A REST API service built with FastAPI to generate personalized daily astrological insights based on user birth details.

## Features

- Infers zodiac sign from birth date.
- Generates personalized insights using a mock LLM (stubbed for future integration).
- Supports English and Hindi output (using dummy translation).
- Includes simple caching with TTL for performance.
- Modular design for easy integration with real Panchang APIs or LLMs like LangChain.

### Requirements

- Python 3.8+
- FastAPI (pip install fastapi)
- Uvicorn (pip install uvicorn)
- Cachetools (pip install cachetools)

### Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd <repo-name>
```


3. Install dependencies:
```
pip install -r requirements.txt
```


5. Run the server:
```
python main.py
```

### Usage
Send a POST request to the API with birth details.

### Example Request (English)
```
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{
  "name": "Ritika",
  "birth_date": "1995-08-20",
  "birth_time": "14:30",
  "birth_place": "Jaipur, India"
}'
```

### Example Response
```
{
  "zodiac": "Leo",
  "insight": "Your innate leadership and warmth will shine today. Embrace spontaneity and avoid overthinking. Your cultural roots in Jaipur, India may guide your decisions.",
  "language": "en"
}
```

### Example Request (Hindi)
```
curl -X POST "http://localhost:8000/predict/hindi" -H "Content-Type: application/json" -d '{
  "name": "Ritika",
  "birth_date": "1995-08-20",
  "birth_time": "14:30",
  "birth_place": "Jaipur, India"
}'
```

### Example Response (Hindi)
```
{
  "zodiac": "Leo",
  "insight": "आज आपका जन्मजात नेतृत्व और गर्मजोशी चमकेगी। सहजता को अपनाएं और अधिक सोचने से बचें।",
  "language": "hi"
}
```

## Design Choices

- Tech Stack: FastAPI for lightweight, async API; Pydantic for input validation.
- Zodiac Logic: Simple date-based zodiac inference, extensible for Panchang data.
- LLM Stub: Mock insight generator with zodiac traits and location-based personalization, ready for LangChain/OpenAI integration.
- Caching: TTLCache for 24-hour caching to simulate daily predictions.
- Hindi Support: Dummy translation function as a placeholder for IndicTrans2/NLLB.
- Extensibility: Modular functions (get_zodiac_sign, generate_insight) for easy replacement with real APIs or models.
- Assumptions: Birth time and place are currently unused in insight generation but included for future Panchang integration.

## Future Enhancements

- Integrate real Panchang API for precise astrological calculations.
- Replace mock LLM with LangChain or HuggingFace models.
- Add vector store (e.g., FAISS) for retrieving insights from an astrological corpus.
- Store user profiles in a database for behavior-based personalization.
- Expand multilingual support with proper translation models.

## Repository Structure
```
├── main.py           # Main API code
├── README.md         # Project documentation
└── requirements.txt  # Dependencies
```
