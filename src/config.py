import os
from dotenv import load_dotenv

load_dotenv()

CHATVOLT_API_KEY = os.getenv("CHATVOLT_API_KEY")
CHATVOLT_BASE_URL = os.getenv("CHATVOLT_BASE_URL", "https://api.chatvolt.ai")

if not CHATVOLT_API_KEY:
    import warnings
    warnings.warn("CHATVOLT_API_KEY not found in environment variables.")
