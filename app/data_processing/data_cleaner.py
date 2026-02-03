"""
Data cleaning engine for blood domain data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from ..config import Config

class DataCleaner:
    """Comprehensive data cleaning and preprocessing engine"""
    
    def __init__(self):
        self.cleaning_stats = {}
        self.duplicate_threshold = 0.95  # Similarity threshold for duplicate detection
    
    def clean_dataset(self, data: pd.DataFrame, cleaning_options: Dict[str, Any] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Perform comprehensive data cleaning"""
        if cleaning_options is None:
            cleaning_options = {
                "remove_duplicates": True,
                "handle_missing": True,
                "standardize_formats": True,
                "remove_outliers": True,
                "validate_data_types": True
            }
        
        cleaned_data = data.copy()
        stats = {
            "original_records": len(data),
            "cleaning_steps": [],
            "records_removed": 0,
            "records_modified": 0
        }
        
        # Step 1: Remove exact duplicates
        if cleaning_options.get("remove_duplicates", True):
            cleaned_data, duplicate_stats = self._remove_duplicates(cleaned_data)
            stats["cleaning_steps"].append(f"Removed {duplicate_stats['duplicates_removed']} duplicates")
            stats["records_removed"] += duplicate_stats["duplicates_removed"]
        
        # Step 2: Handle missing values
        if cleaning_options.get("handle_missing", True):
            cleaned_data, missing_stats = self._handle_missing_values(cleaned_data)
            stats["cleaning_steps"].append(f"Handled missing values in {missing_stats['fields_processed']} fields")
            stats["records_modified"] += missing_stats["records_modified"]
        
        # Step 3: Standardize formats
        if cleaning_options.get("standardize_formats", True):
            cleaned_data, format_stats = self._standardize_formats(cleaned_data)
            stats["cleaning_steps"].append(f"Standardized formats for {format_stats['fields_processed']} fields")
            stats["records_modified"] += format_stats["records_modified"]
        
        # Step 4: Remove outliers
        if cleaning_options.get("remove_outliers", True):
            cleaned_data, outlier_stats = self._remove_outliers(cleaned_data)
            stats["cleaning_steps"].append(f"Removed {outlier_stats['outliers_removed']} outliers")
            stats["records_removed"] += outlier_stats["outliers_removed"]
        
        # Step 5: Validate and fix data types
        if cleaning_options.get("validate_data_types", True):
            cleaned_data, type_stats = self._validate_and_fix_types(cleaned_data)
            stats["cleaning_steps"].append(f"Fixed data types for {type_stats['fields_processed']} fields")
            stats["records_modified"] += type_stats["records_modified"]
        
        stats["final_records"] = len(cleaned_data)
        stats["data_quality_score"] = self._calculate_quality_score(data, cleaned_data)
        
        return cleaned_data, stats
    
    def _remove_duplicates(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """Remove duplicate records"""
        original_count = len(data)
        
        # Remove exact duplicates
        data_deduped = data.drop_duplicates()
        exact_duplicates_removed = original_count - len(data_deduped)
        
        # Remove near-duplicates based on key fields
        key_fields = ["name", "contact_number", "email", "blood_type"]
        available_key_fields = [field for field in key_fields if field in data.columns]
        
        if available_key_fields:
            # Create a composite key for duplicate detection
            data_deduped["duplicate_key"] = data_deduped[available_key_fields].astype(str).agg('|'.join, axis=1)
            near_duplicates_removed = len(data_deduped) - len(data_deduped.drop_duplicates(subset=["duplicate_key"]))
            data_deduped = data_deduped.drop_duplicates(subset=["duplicate_key"])
            data_deduped = data_deduped.drop(columns=["duplicate_key"])
        else:
            near_duplicates_removed = 0
        
        total_duplicates_removed = exact_duplicates_removed + near_duplicates_removed
        
        return data_deduped, {
            "duplicates_removed": total_duplicates_removed,
            "exact_duplicates": exact_duplicates_removed,
            "near_duplicates": near_duplicates_removed
        }
    
    def _handle_missing_values(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Handle missing values based on field importance and data type"""
        cleaned_data = data.copy()
        records_modified = 0
        fields_processed = 0
        
        # Define strategies for different field types
        missing_strategies = {
            "name": {"strategy": "remove", "threshold": 0.1},  # Remove if >10% missing
            "age": {"strategy": "median", "threshold": 0.3},
            "blood_type": {"strategy": "mode", "threshold": 0.2},
            "contact_number": {"strategy": "remove", "threshold": 0.1},
            "email": {"strategy": "remove", "threshold": 0.3},
            "donation_date": {"strategy": "remove", "threshold": 0.05},
            "volume_ml": {"strategy": "median", "threshold": 0.2},
            "hemoglobin_level": {"strategy": "median", "threshold": 0.4},
            "blood_pressure_systolic": {"strategy": "median", "threshold": 0.4},
            "blood_pressure_diastolic": {"strategy": "median", "threshold": 0.4}
        }
        
        for column in cleaned_data.columns:
            if column not in missing_strategies:
                continue
            
            missing_ratio = cleaned_data[column].isna().sum() / len(cleaned_data)
            strategy = missing_strategies[column]
            
            if missing_ratio > strategy["threshold"]:
                # Too many missing values, remove column
                cleaned_data = cleaned_data.drop(columns=[column])
                fields_processed += 1
                continue
            
            if missing_ratio == 0:
                continue  # No missing values
            
            fields_processed += 1
            
            if strategy["strategy"] == "remove":
                # Remove rows with missing values in critical fields
                before_count = len(cleaned_data)
                cleaned_data = cleaned_data.dropna(subset=[column])
                records_modified += before_count - len(cleaned_data)
            
            elif strategy["strategy"] == "mode":
                # Fill with most frequent value
                mode_value = cleaned_data[column].mode()
                if not mode_value.empty:
                    cleaned_data[column] = cleaned_data[column].fillna(mode_value[0])
                    records_modified += cleaned_data[column].isna().sum()
            
            elif strategy["strategy"] == "median":
                # Fill with median value for numeric fields
                if cleaned_data[column].dtype in ['int64', 'float64']:
                    median_value = cleaned_data[column].median()
                    cleaned_data[column] = cleaned_data[column].fillna(median_value)
                    records_modified += cleaned_data[column].isna().sum()
            
            elif strategy["strategy"] == "forward_fill":
                # Forward fill for time series data
                cleaned_data[column] = cleaned_data[column].fillna(method='ffill')
                records_modified += cleaned_data[column].isna().sum()
        
        return cleaned_data, {
            "fields_processed": fields_processed,
            "records_modified": records_modified
        }
    
    def _standardize_formats(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Standardize data formats across fields"""
        cleaned_data = data.copy()
        records_modified = 0
        fields_processed = 0
        
        # Standardize blood type format
        if "blood_type" in cleaned_data.columns:
            before = cleaned_data["blood_type"].copy()
            cleaned_data["blood_type"] = cleaned_data["blood_type"].astype(str).str.upper().str.strip()
            # Standardize variations
            blood_type_mapping = {
                "A POSITIVE": "A+", "A POS": "A+", "A+": "A+",
                "A NEGATIVE": "A-", "A NEG": "A-", "A-": "A-",
                "B POSITIVE": "B+", "B POS": "B+", "B+": "B+",
                "B NEGATIVE": "B-", "B NEG": "B-", "B-": "B-",
                "AB POSITIVE": "AB+", "AB POS": "AB+", "AB+": "AB+",
                "AB NEGATIVE": "AB-", "AB NEG": "AB-", "AB-": "AB-",
                "O POSITIVE": "O+", "O POS": "O+", "O+": "O+",
                "O NEGATIVE": "O-", "O NEG": "O-", "O-": "O-"
            }
            cleaned_data["blood_type"] = cleaned_data["blood_type"].map(blood_type_mapping).fillna(cleaned_data["blood_type"])
            records_modified += sum(before != cleaned_data["blood_type"])
            fields_processed += 1
        
        # Standardize phone numbers
        if "contact_number" in cleaned_data.columns:
            before = cleaned_data["contact_number"].copy()
            # Remove all non-numeric characters
            cleaned_data["contact_number"] = cleaned_data["contact_number"].astype(str).str.replace(r'[^\d]', '', regex=True)
            # Standardize length (assuming 10-digit numbers)
            cleaned_data["contact_number"] = cleaned_data["contact_number"].str[-10:]
            records_modified += sum(before != cleaned_data["contact_number"])
            fields_processed += 1
        
        # Standardize email format
        if "email" in cleaned_data.columns:
            before = cleaned_data["email"].copy()
            cleaned_data["email"] = cleaned_data["email"].astype(str).str.lower().str.strip()
            records_modified += sum(before != cleaned_data["email"])
            fields_processed += 1
        
        # Standardize gender
        if "gender" in cleaned_data.columns:
            before = cleaned_data["gender"].copy()
            gender_mapping = {
                "M": "male", "MALE": "male", "MAN": "male", "men": "male",
                "F": "female", "FEMALE": "female", "WOMAN": "female", "women": "female",
                "O": "other", "OTHER": "other"
            }
            cleaned_data["gender"] = cleaned_data["gender"].astype(str).str.upper().map(gender_mapping).fillna(cleaned_data["gender"])
            records_modified += sum(before != cleaned_data["gender"])
            fields_processed += 1
        
        # Standardize date formats
        date_fields = ["donation_date", "registration_date", "last_donation_date", "birth_date"]
        for field in date_fields:
            if field in cleaned_data.columns:
                try:
                    before = cleaned_data[field].copy()
                    cleaned_data[field] = pd.to_datetime(cleaned_data[field], errors='coerce')
                    records_modified += sum(before != cleaned_data[field])
                    fields_processed += 1
                except:
                    continue
        
        return cleaned_data, {
            "fields_processed": fields_processed,
            "records_modified": records_modified
        }
    
    def _remove_outliers(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """Remove outliers using IQR method"""
        cleaned_data = data.copy()
        outliers_removed = 0
        
        # Numeric fields to check for outliers
        numeric_fields = ["age", "volume_ml", "hemoglobin_level", "blood_pressure_systolic", "blood_pressure_diastolic", "pulse_rate", "temperature"]
        
        for field in numeric_fields:
            if field not in cleaned_data.columns or cleaned_data[field].dtype not in ['int64', 'float64']:
                continue
            
            Q1 = cleaned_data[field].quantile(0.25)
            Q3 = cleaned_data[field].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Identify outliers
            outliers = (cleaned_data[field] < lower_bound) | (cleaned_data[field] > upper_bound)
            outliers_count = outliers.sum()
            
            if outliers_count > 0:
                # Remove outliers
                cleaned_data = cleaned_data[~outliers]
                outliers_removed += outliers_count
        
        return cleaned_data, {
            "outliers_removed": outliers_removed
        }
    
    def _validate_and_fix_types(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Validate and fix data types"""
        cleaned_data = data.copy()
        records_modified = 0
        fields_processed = 0
        
        # Expected data types for blood domain
        type_mapping = {
            "age": "int64",
            "volume_ml": "float64",
            "hemoglobin_level": "float64",
            "blood_pressure_systolic": "int64",
            "blood_pressure_diastolic": "int64",
            "pulse_rate": "int64",
            "temperature": "float64",
            "is_successful": "bool",
            "is_active": "bool"
        }
        
        for field, expected_type in type_mapping.items():
            if field not in cleaned_data.columns:
                continue
            
            try:
                before = cleaned_data[field].copy()
                
                if expected_type == "int64":
                    cleaned_data[field] = pd.to_numeric(cleaned_data[field], errors='coerce').astype('Int64')
                elif expected_type == "float64":
                    cleaned_data[field] = pd.to_numeric(cleaned_data[field], errors='coerce')
                elif expected_type == "bool":
                    cleaned_data[field] = cleaned_data[field].astype(str).str.lower().map({
                        'true': True, '1': True, 'yes': True, 'y': True,
                        'false': False, '0': False, 'no': False, 'n': False
                    }).fillna(False)
                
                records_modified += sum(before != cleaned_data[field])
                fields_processed += 1
                
            except Exception as e:
                print(f"Error converting {field} to {expected_type}: {e}")
                continue
        
        return cleaned_data, {
            "fields_processed": fields_processed,
            "records_modified": records_modified
        }
    
    def _calculate_quality_score(self, original_data: pd.DataFrame, cleaned_data: pd.DataFrame) -> float:
        """Calculate overall data quality score"""
        if original_data.empty:
            return 0.0
        
        # Factors affecting quality score
        completeness_score = 100 - (original_data.isna().sum().sum() / (len(original_data) * len(original_data.columns)) * 100)
        consistency_score = 95.0  # Placeholder for consistency checks
        validity_score = 90.0   # Placeholder for validity checks
        
        # Deduplication score
        dedup_score = (len(cleaned_data) / len(original_data)) * 100 if len(original_data) > 0 else 0
        
        # Weighted average
        overall_score = (completeness_score * 0.3 + consistency_score * 0.2 + 
                        validity_score * 0.3 + dedup_score * 0.2)
        
        return round(overall_score, 2)
