"""
Configuration settings for the regression testing library.
"""

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "regression_tests"

# Tolerance threshold for pass/fail determination (as a decimal percentage)
TOLERANCE_THRESHOLD = 0.05  # 5% tolerance