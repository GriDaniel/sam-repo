import os

# Database Configuration
DB_URI = os.getenv("DB_URI", "mongodb://localhost:27017/")  # MongoDB URI
DB_NAME = os.getenv("DB_NAME", "samreglib_db")  # MongoDB Database name

# Tolerance Level for Comparator (Percentage tolerance)
TOLERANCE_LEVEL = float(os.getenv("TOLERANCE_LEVEL", 0.05))  # Default 5% tolerance

