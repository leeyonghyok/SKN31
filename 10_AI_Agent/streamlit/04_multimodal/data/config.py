from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")

MODEL_NAME = 'gpt-4o-mini'