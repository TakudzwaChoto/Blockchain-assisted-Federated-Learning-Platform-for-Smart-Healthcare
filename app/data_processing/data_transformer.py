"""
Data transformation engine for blood domain data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from ..config import Config

class DataTransformer:
    """Data transformation and feature engineering engine"""
    
    def __init__(self):
        self.transformation_log = []
    
    def transform_dataset(self, data: pd.DataFrame, transformation_config: Dict[str, Any] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Perform comprehensive data transformation"""
        if transformation_config is None:
            transformation_config = {
                "create_derived_fields": True,
                "normalize_data": True,
                "aggregate_data": False,
                "encode_categorical": True,
                "create_time_features": True
            }
        
        transformed_data = data.copy()
        transformations_applied = []
        
        # Step 1: Create derived fields
        if transformation_config.get("create_derived_fields", True):
            transformed_data = self._create_derived_fields(transformed_data)
            transformations_applied.append("Created derived fields")
        
        # Step 2: Encode categorical variables
        if transformation_config.get("encode_categorical", True):
            transformed_data = self._encode_categorical_variables(transformed_data)
            transformations_applied.append("Encoded categorical variables")
        
        # Step 3: Create time-based features
        if transformation_config.get("create_time_features", True):
            transformed_data = self._create_time_features(transformed_data)
            transformations_applied.append("Created time-based features")
        
        # Step 4: Normalize/standardize numerical fields
        if transformation_config.get("normalize_data", True):
            transformed_data = self._normalize_numerical_fields(transformed_data)
            transformations_applied.append("Normalized numerical fields")
        
        # Step 5: Aggregate data if requested
        if transformation_config.get("aggregate_data", False):
            transformed_data = self._aggregate_data(transformed_data, transformation_config.get("aggregation_level", "daily"))
            transformations_applied.append(f"Aggregated data to {transformation_config.get('aggregation_level', 'daily')} level")
        
        transformation_summary = {
            "original_shape": data.shape,
            "transformed_shape": transformed_data.shape,
            "transformations_applied": transformations_applied,
            "new_features": self._get_new_features(data, transformed_data),
            "transformation_timestamp": datetime.now()
        }
        
        return transformed_data, transformation_summary
    
    def _create_derived_fields(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create derived fields for blood domain analysis"""
        transformed_data = data.copy()
        
        # Age groups
        if "age" in transformed_data.columns:
            transformed_data["age_group"] = pd.cut(
                transformed_data["age"],
                bins=[0, 25, 35, 45, 55, 65, 100],
                labels=["18-25", "26-35", "36-45", "46-55", "56-65", "65+"],
                include_lowest=True
            )
        
        # Donation volume categories
        if "volume_ml" in transformed_data.columns:
            transformed_data["volume_category"] = pd.cut(
                transformed_data["volume_ml"],
                bins=[0, 350, 450, 600],
                labels=["Low", "Standard", "High"],
                include_lowest=True
            )
        
        # Hemoglobin status
        if "hemoglobin_level" in transformed_data.columns:
            transformed_data["hemoglobin_status"] = pd.cut(
                transformed_data["hemoglobin_level"],
                bins=[0, 12.5, 15.5, 20],
                labels=["Low", "Normal", "High"],
                include_lowest=True
            )
        
        # Blood pressure categories
        if all(col in transformed_data.columns for col in ["blood_pressure_systolic", "blood_pressure_diastolic"]):
            def bp_category(row):
                systolic = row["blood_pressure_systolic"]
                diastolic = row["blood_pressure_diastolic"]
                if pd.isna(systolic) or pd.isna(diastolic):
                    return "Unknown"
                if systolic < 120 and diastolic < 80:
                    return "Normal"
                elif systolic < 140 and diastolic < 90:
                    return "Elevated"
                elif systolic < 180 and diastolic < 120:
                    return "High"
                else:
                    return "Very High"
            
            transformed_data["blood_pressure_category"] = transformed_data.apply(bp_category, axis=1)
        
        # BMI calculation (if height and weight available)
        if all(col in transformed_data.columns for col in ["height_cm", "weight_kg"]):
            transformed_data["bmi"] = transformed_data["weight_kg"] / ((transformed_data["height_cm"] / 100) ** 2)
            transformed_data["bmi_category"] = pd.cut(
                transformed_data["bmi"],
                bins=[0, 18.5, 25, 30, 40],
                labels=["Underweight", "Normal", "Overweight", "Obese"],
                include_lowest=True
            )
        
        # Donor eligibility score
        transformed_data["eligibility_score"] = self._calculate_eligibility_score(transformed_data)
        
        # Seasonal indicators
        if "donation_date" in transformed_data.columns:
            transformed_data["season"] = pd.to_datetime(transformed_data["donation_date"]).dt.month.map({
                12: "Winter", 1: "Winter", 2: "Winter",
                3: "Spring", 4: "Spring", 5: "Spring",
                6: "Summer", 7: "Summer", 8: "Summer",
                9: "Fall", 10: "Fall", 11: "Fall"
            })
        
        # Day of week analysis
        if "donation_date" in transformed_data.columns:
            transformed_data["day_of_week"] = pd.to_datetime(transformed_data["donation_date"]).dt.day_name()
            transformed_data["is_weekend"] = pd.to_datetime(transformed_data["donation_date"]).dt.dayofweek >= 5
        
        return transformed_data
    
    def _encode_categorical_variables(self, data: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical variables for machine learning"""
        transformed_data = data.copy()
        
        # Blood type encoding (Rh factor and ABO group)
        if "blood_type" in transformed_data.columns:
            transformed_data["rh_factor"] = transformed_data["blood_type"].astype(str).apply(lambda x: 1 if "+" in str(x) else 0)
            transformed_data["abo_group"] = transformed_data["blood_type"].astype(str).str.replace("+", "").replace("-", "")
        
        # One-hot encode categorical variables
        categorical_fields = ["gender", "donation_type", "category", "age_group", "volume_category", 
                            "hemoglobin_status", "blood_pressure_category", "season", "day_of_week"]
        
        for field in categorical_fields:
            if field in transformed_data.columns:
                dummies = pd.get_dummies(transformed_data[field], prefix=field)
                transformed_data = pd.concat([transformed_data, dummies], axis=1)
        
        return transformed_data
    
    def _create_time_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create time-based features for analysis"""
        transformed_data = data.copy()
        
        if "donation_date" in transformed_data.columns:
            donation_dates = pd.to_datetime(transformed_data["donation_date"])
            
            # Basic time features
            transformed_data["year"] = donation_dates.dt.year
            transformed_data["month"] = donation_dates.dt.month
            transformed_data["quarter"] = donation_dates.dt.quarter
            transformed_data["week_of_year"] = donation_dates.dt.isocalendar().week
            transformed_data["day_of_year"] = donation_dates.dt.dayofyear
            
            # Cyclical features
            transformed_data["month_sin"] = np.sin(2 * np.pi * donation_dates.dt.month / 12)
            transformed_data["month_cos"] = np.cos(2 * np.pi * donation_dates.dt.month / 12)
            transformed_data["day_sin"] = np.sin(2 * np.pi * donation_dates.dt.day / 31)
            transformed_data["day_cos"] = np.cos(2 * np.pi * donation_dates.dt.day / 31)
            
            # Special dates
            transformed_data["is_holiday_season"] = donation_dates.dt.month.isin([11, 12])
            transformed_data["is_summer"] = donation_dates.dt.month.isin([6, 7, 8])
        
        # Time since last donation
        if "last_donation_date" in transformed_data.columns and "donation_date" in transformed_data.columns:
            transformed_data["days_since_last_donation"] = (
                pd.to_datetime(transformed_data["donation_date"]) - 
                pd.to_datetime(transformed_data["last_donation_date"])
            ).dt.days
            transformed_data["days_since_last_donation"] = transformed_data["days_since_last_donation"].fillna(365)
        
        # Time since registration
        if "registration_date" in transformed_data.columns and "donation_date" in transformed_data.columns:
            transformed_data["days_since_registration"] = (
                pd.to_datetime(transformed_data["donation_date"]) - 
                pd.to_datetime(transformed_data["registration_date"])
            ).dt.days
        
        return transformed_data
    
    def _normalize_numerical_fields(self, data: pd.DataFrame) -> pd.DataFrame:
        """Normalize numerical fields for analysis"""
        transformed_data = data.copy()
        
        # Fields to normalize
        numerical_fields = ["age", "volume_ml", "hemoglobin_level", "blood_pressure_systolic", 
                           "blood_pressure_diastolic", "pulse_rate", "temperature", "days_since_last_donation",
                           "days_since_registration", "eligibility_score"]
        
        for field in numerical_fields:
            if field in transformed_data.columns and transformed_data[field].dtype in ['int64', 'float64']:
                # Min-max normalization
                min_val = transformed_data[field].min()
                max_val = transformed_data[field].max()
                if max_val != min_val:
                    transformed_data[f"{field}_normalized"] = (transformed_data[field] - min_val) / (max_val - min_val)
                else:
                    transformed_data[f"{field}_normalized"] = 0.5
        
        return transformed_data
    
    def _aggregate_data(self, data: pd.DataFrame, aggregation_level: str = "daily") -> pd.DataFrame:
        """Aggregate data by time period"""
        if "donation_date" not in data.columns:
            return data
        
        data_copy = data.copy()
        data_copy["donation_date"] = pd.to_datetime(data_copy["donation_date"])
        
        if aggregation_level == "daily":
            data_copy["period"] = data_copy["donation_date"].dt.date
        elif aggregation_level == "weekly":
            data_copy["period"] = data_copy["donation_date"].dt.to_period('W')
        elif aggregation_level == "monthly":
            data_copy["period"] = data_copy["donation_date"].dt.to_period('M')
        elif aggregation_level == "quarterly":
            data_copy["period"] = data_copy["donation_date"].dt.to_period('Q')
        elif aggregation_level == "yearly":
            data_copy["period"] = data_copy["donation_date"].dt.to_period('Y')
        
        # Define aggregation functions
        agg_functions = {
            "volume_ml": ["sum", "mean", "count"],
            "donor_id": "nunique",
            "age": "mean",
            "hemoglobin_level": "mean",
            "eligibility_score": "mean"
        }
        
        # Apply aggregation
        available_functions = {k: v for k, v in agg_functions.items() if k in data_copy.columns}
        
        if available_functions:
            aggregated_data = data_copy.groupby("period").agg(available_functions).reset_index()
            
            # Flatten column names
            aggregated_data.columns = ['_'.join(col).strip() if col[1] else col[0] for col in aggregated_data.columns]
            aggregated_data = aggregated_data.rename(columns={"period_": "period"})
            
            return aggregated_data
        
        return data
    
    def _calculate_eligibility_score(self, data: pd.DataFrame) -> pd.Series:
        """Calculate donor eligibility score based on various factors"""
        scores = []
        
        for _, row in data.iterrows():
            score = 100  # Start with perfect score
            
            # Age factor
            if "age" in data.columns and pd.notna(row["age"]):
                age = row["age"]
                if age < 20 or age > 60:
                    score -= 20
                elif age < 25 or age > 55:
                    score -= 10
            
            # Hemoglobin factor
            if "hemoglobin_level" in data.columns and pd.notna(row["hemoglobin_level"]):
                hgb = row["hemoglobin_level"]
                if hgb < 12.5 or hgb > 16.0:
                    score -= 15
                elif hgb < 13.0 or hgb > 15.5:
                    score -= 5
            
            # Blood pressure factor
            if all(col in data.columns and pd.notna(row[col]) for col in ["blood_pressure_systolic", "blood_pressure_diastolic"]):
                systolic = row["blood_pressure_systolic"]
                diastolic = row["blood_pressure_diastolic"]
                if systolic > 140 or diastolic > 90:
                    score -= 15
                elif systolic > 130 or diastolic > 85:
                    score -= 5
            
            # Recent donation factor
            if "days_since_last_donation" in data.columns and pd.notna(row["days_since_last_donation"]):
                days_since = row["days_since_last_donation"]
                if days_since < 56:
                    score -= 50  # Not eligible
                elif days_since < 90:
                    score -= 10  # Recently donated
            
            scores.append(max(0, score))
        
        return pd.Series(scores)
    
    def _get_new_features(self, original_data: pd.DataFrame, transformed_data: pd.DataFrame) -> List[str]:
        """Get list of new features created during transformation"""
        original_columns = set(original_data.columns)
        transformed_columns = set(transformed_data.columns)
        new_features = transformed_columns - original_columns
        return sorted(list(new_features))
    
    def create_unified_schema(self, datasets: List[pd.DataFrame], source_names: List[str]) -> pd.DataFrame:
        """Create unified schema from multiple blood center datasets"""
        unified_data = pd.DataFrame()
        
        for i, (data, source_name) in enumerate(zip(datasets, source_names)):
            data_copy = data.copy()
            data_copy["source_system"] = source_name
            data_copy["source_id"] = i
            
            # Standardize field names across systems
            field_mapping = self._get_field_mapping(data_copy.columns)
            data_copy = data_copy.rename(columns=field_mapping)
            
            if unified_data.empty:
                unified_data = data_copy
            else:
                unified_data = pd.concat([unified_data, data_copy], ignore_index=True)
        
        return unified_data
    
    def _get_field_mapping(self, columns: List[str]) -> Dict[str, str]:
        """Get field mapping for standardization across systems"""
        mapping = {}
        
        # Common field variations and their standard names
        field_variations = {
            "donor_name": ["name", "donor_name", "patient_name", "full_name"],
            "donor_age": ["age", "donor_age", "patient_age", "age_years"],
            "donor_gender": ["gender", "sex", "donor_gender", "patient_sex"],
            "blood_type": ["blood_type", "blood_group", "btype", "group"],
            "contact_number": ["phone", "telephone", "mobile", "contact", "phone_number"],
            "email": ["email", "email_address", "mail", "email_id"],
            "donation_date": ["date", "donation_date", "collection_date", "donated_on"],
            "donation_type": ["type", "donation_type", "collection_type", "product_type"],
            "volume_ml": ["volume", "donation_volume", "ml", "amount"],
            "location": ["center", "location", "facility", "clinic", "hospital"]
        }
        
        for standard_name, variations in field_variations.items():
            for col in columns:
                if col.lower() in [v.lower() for v in variations]:
                    mapping[col] = standard_name
                    break
        
        return mapping
