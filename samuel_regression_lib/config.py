"""
Configuration settings for Samuel Regression Testing Library.
"""

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "samuel_regression"
MONGO_COLLECTION_PREFIX = "reference_data_"  # Will be combined with method name

# Testing threshold settings
TOLERANCE_THRESHOLD = 0.01  # 1% tolerance for numerical comparisons

# Logging settings
ENABLE_DEBUG_LOGGING = False