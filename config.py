import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Server Config
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# MongoDB Config (Optional: if empty or connection fails, falls back to JsonDataStore seamlessly)
MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "facultyflow")

# Secret key for sessions/tokens (dummy secret for demo)
SECRET_KEY = os.getenv("SECRET_KEY", "facultyflow-college-project-secret-2026")
