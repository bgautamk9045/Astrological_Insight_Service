from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
from typing import Dict
from cachetools import TTLCache
import uuid
import uvicorn

app = FastAPI()

# Input model
class BirthDetails(BaseModel):
    name: str
    birth_date: str
    birth_time: str
    birth_place: str

# Output model
class AstroInsight(BaseModel):
    zodiac: str
    insight: str
    language: str

# Simple cache: stores results for 24 hours
cache = TTLCache(maxsize=100, ttl=86400)

# Zodiac inference logic
def get_zodiac_sign(birth_date: str) -> str:
    try:
        date = datetime.strptime(birth_date, "%Y-%m-%d")
        day = date.day
        month = date.month
        zodiac_ranges = [
            ((1, 20), (2, 18), "Aquarius"),
            ((2, 19), (3, 20), "Pisces"),
            ((3, 21), (4, 19), "Aries"),
            ((4, 20), (5, 20), "Taurus"),
            ((5, 21), (6, 20), "Gemini"),
            ((6, 21), (7, 22), "Cancer"),
            ((7, 23), (8, 22), "Leo"),
            ((8, 23), (9, 22), "Virgo"),
            ((9, 23), (10, 22), "Libra"),
            ((10, 23), (11, 21), "Scorpio"),
            ((11, 22), (12, 21), "Sagittarius"),
            ((12, 22), (1, 19), "Capricorn"),
        ]
        for start, end, sign in zodiac_ranges:
            if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
                return sign
        return "Capricorn"  # Edge case for Dec-Jan
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid birth_date format. Use YYYY-MM-DD")

# Mock LLM response generator
def generate_insight(zodiac: str, name: str, birth_place: str, language: str = "en") -> str:
    zodiac_traits = {
        "Leo": "leadership and warmth",
        "Virgo": "precision and practicality",
        "Libra": "balance and charm",
        # Add other zodiac traits as needed
    }
    trait = zodiac_traits.get(zodiac, "confidence and resilience")
    base_insight = f"Your innate {trait} will shine today. Embrace spontaneity and avoid overthinking."
    
    # Simulate personalization
    if "India" in birth_place:
        base_insight += f" Your cultural roots in {birth_place} may guide your decisions."
    
    # Simulate LLM call (replace with LangChain/OpenAI later)
    if language == "hi":
        return translate_to_hindi(base_insight)
    return base_insight

# Dummy translation function (stub for IndicTrans2/NLLB)
def translate_to_hindi(text: str) -> str:
    # Placeholder: In reality, use IndicTrans2 or NLLB
    translations = {
        "Your innate leadership and warmth will shine today. Embrace spontaneity and avoid overthinking.": 
        "आज आपका जन्मजात नेतृत्व और गर्मजोशी चमकेगी। सहजता को अपनाएं और अधिक सोचने से बचें।"
    }
    return translations.get(text, text)

# REST API endpoint
@app.post("/predict", response_model=AstroInsight)
async def predict_insight(details: BirthDetails):
    cache_key = f"{details.name}_{details.birth_date}_{details.birth_place}"
    
    # Check cache
    if cache_key in cache:
        return cache[cache_key]
    
    # Generate response
    zodiac = get_zodiac_sign(details.birth_date)
    insight = generate_insight(zodiac, details.name, details.birth_place, language="en")
    
    response = AstroInsight(zodiac=zodiac, insight=insight, language="en")
    cache[cache_key] = response
    return response

# Hindi endpoint
@app.post("/predict/hindi", response_model=AstroInsight)
async def predict_insight_hindi(details: BirthDetails):
    cache_key = f"{details.name}_{details.birth_date}_{details.birth_place}_hi"
    
    # Check cache
    if cache_key in cache:
        return cache[cache_key]
    
    # Generate response
    zodiac = get_zodiac_sign(details.birth_date)
    insight = generate_insight(zodiac, details.name, details.birth_place, language="hi")
    
    response = AstroInsight(zodiac=zodiac, insight=insight, language="hi")
    cache[cache_key] = response
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)