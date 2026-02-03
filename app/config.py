"""
Configuration settings for Blood Domain Engine
"""

import os
from typing import Dict, Any

class Config:
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/blood_domain")
    
    # Data processing settings
    MAX_BATCH_SIZE = 1000000  # 1 million records per batch
    SUPPORTED_FORMATS = ["csv", "excel", "json", "sql", "api"]
    
    # Blood type standards
    BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    
    # Donation types
    DONATION_TYPES = ["whole_blood", "platelets", "plasma", "red_blood_cells"]
    
    # Donor categories
    DONOR_CATEGORIES = ["individual", "group", "military", "student", "healthcare", "civil_servant"]
    
    # Analysis settings
    FORECASTING_MODELS = ["arima", "prophet", "lstm", "linear_regression"]
    CLUSTERING_ALGORITHMS = ["kmeans", "dbscan"]
    CLASSIFICATION_ALGORITHMS = ["decision_tree", "svm", "random_forest"]
    
    # Visualization settings
    CHART_TYPES = ["bar", "line", "pie", "radar", "heatmap", "scatter"]
    EXPORT_FORMATS = ["pdf", "png", "excel", "csv"]
    
    # API settings
    API_PREFIX = "/api/v1"
    
    # File upload settings
    UPLOAD_FOLDER = "uploads"
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    
    @classmethod
    def get_validation_rules(cls) -> Dict[str, Any]:
        """Return data validation rules"""
        return {
            "blood_type": {
                "type": "string",
                "allowed": cls.BLOOD_TYPES,
                "required": True
            },
            "donation_date": {
                "type": "datetime",
                "required": True
            },
            "donor_age": {
                "type": "integer",
                "min": 18,
                "max": 65,
                "required": True
            },
            "donation_volume": {
                "type": "float",
                "min": 200,
                "max": 500,
                "required": True
            }
        }
