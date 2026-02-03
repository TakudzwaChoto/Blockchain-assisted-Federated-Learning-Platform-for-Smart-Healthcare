"""
Data validation engine for blood domain data
"""

import re
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from ..models.validation import DataRule, ValidationResult, BatchValidationResult, ValidationSeverity, BLOOD_DOMAIN_RULES, BLOOD_CONSISTENCY_RULES
from ..config import Config

class DataValidator:
    """Comprehensive data validation engine"""
    
    def __init__(self):
        self.rules = BLOOD_DOMAIN_RULES.copy()
        self.consistency_rules = BLOOD_CONSISTENCY_RULES.copy()
        self.custom_rules = []
    
    def add_rule(self, rule: DataRule) -> None:
        """Add a custom validation rule"""
        self.custom_rules.append(rule)
    
    def validate_batch(self, data: pd.DataFrame, batch_id: str) -> BatchValidationResult:
        """Validate entire batch of data"""
        start_time = datetime.now()
        all_results = []
        
        # Validate each record
        for idx, row in data.iterrows():
            record_results = self.validate_record(row, str(idx))
            all_results.extend(record_results)
        
        # Calculate summary statistics
        total_records = len(data)
        invalid_records = len(set(r.record_id for r in all_results if not r.is_valid))
        valid_records = total_records - invalid_records
        
        # Group by severity
        severity_summary = {}
        for result in all_results:
            severity = result.severity.value
            severity_summary[severity] = severity_summary.get(severity, 0) + 1
        
        # Group by rule
        rule_summary = {}
        for result in all_results:
            rule_name = result.rule_name
            if rule_name not in rule_summary:
                rule_summary[rule_name] = {"valid": 0, "invalid": 0}
            if result.is_valid:
                rule_summary[rule_name]["valid"] += 1
            else:
                rule_summary[rule_name]["invalid"] += 1
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return BatchValidationResult(
            batch_id=batch_id,
            total_records=total_records,
            valid_records=valid_records,
            invalid_records=invalid_records,
            validation_results=all_results,
            summary_by_severity=severity_summary,
            summary_by_rule=rule_summary,
            processing_time_seconds=processing_time
        )
    
    def validate_record(self, record: pd.Series, record_id: str) -> List[ValidationResult]:
        """Validate a single record against all rules"""
        results = []
        all_rules = self.rules + self.custom_rules
        
        for rule in all_rules:
            if not rule.is_active:
                continue
                
            result = self._apply_rule(record, rule, record_id)
            results.append(result)
        
        # Apply consistency rules
        consistency_results = self._apply_consistency_rules(record, record_id)
        results.extend(consistency_results)
        
        return results
    
    def _apply_rule(self, record: pd.Series, rule: DataRule, record_id: str) -> ValidationResult:
        """Apply a single validation rule to a record"""
        field_value = record.get(rule.field_name)
        is_valid = True
        message = "Validation passed"
        error_details = None
        
        try:
            if rule.rule_type.value == "data_type":
                is_valid = self._validate_data_type(field_value, rule)
            elif rule.rule_type.value == "range_check":
                is_valid, error_details = self._validate_range(field_value, rule)
            elif rule.rule_type.value == "format_validation":
                is_valid, error_details = self._validate_format(field_value, rule)
            elif rule.rule_type.value == "business_rule":
                is_valid, error_details = self._validate_business_rule(record, rule)
            
            if not is_valid:
                message = f"Rule '{rule.name}' failed: {rule.description}"
                
        except Exception as e:
            is_valid = False
            message = f"Validation error: {str(e)}"
            error_details = {"exception": str(e)}
        
        return ValidationResult(
            rule_id=rule.id or "unknown",
            rule_name=rule.name,
            field_name=rule.field_name,
            record_id=record_id,
            actual_value=field_value,
            expected_value=rule.expected_value,
            is_valid=is_valid,
            severity=rule.severity,
            message=message,
            error_details=error_details
        )
    
    def _validate_data_type(self, value: Any, rule: DataRule) -> bool:
        """Validate data type"""
        if pd.isna(value):
            return True  # Let null validation be handled separately
        
        expected_type = rule.expected_value
        if expected_type == "string":
            return isinstance(value, str)
        elif expected_type == "integer":
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        elif expected_type == "float":
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        elif expected_type == "datetime":
            return isinstance(value, (datetime, pd.Timestamp))
        elif expected_type == "boolean":
            return isinstance(value, bool)
        
        return True
    
    def _validate_range(self, value: Any, rule: DataRule) -> Tuple[bool, Optional[Dict]]:
        """Validate value range"""
        if pd.isna(value):
            return True, None
        
        try:
            numeric_value = float(value)
        except (ValueError, TypeError):
            return False, {"error": "Value cannot be converted to number"}
        
        if rule.min_value is not None and numeric_value < rule.min_value:
            return False, {"error": f"Value {numeric_value} below minimum {rule.min_value}"}
        
        if rule.max_value is not None and numeric_value > rule.max_value:
            return False, {"error": f"Value {numeric_value} above maximum {rule.max_value}"}
        
        return True, None
    
    def _validate_format(self, value: Any, rule: DataRule) -> Tuple[bool, Optional[Dict]]:
        """Validate format using regex or allowed values"""
        if pd.isna(value):
            return True, None
        
        str_value = str(value)
        
        if rule.allowed_values:
            return str_value in rule.allowed_values, {
                "error": f"Value '{str_value}' not in allowed values: {rule.allowed_values}"
            }
        
        if rule.pattern:
            pattern = re.compile(rule.pattern)
            return bool(pattern.match(str_value)), {
                "error": f"Value '{str_value}' does not match required pattern"
            }
        
        return True, None
    
    def _validate_business_rule(self, record: pd.Series, rule: DataRule) -> Tuple[bool, Optional[Dict]]:
        """Validate business logic rules"""
        # This would contain domain-specific business logic
        # For now, return True as placeholder
        return True, None
    
    def _apply_consistency_rules(self, record: pd.Series, record_id: str) -> List[ValidationResult]:
        """Apply cross-field consistency rules"""
        results = []
        
        for rule in self.consistency_rules:
            if not rule.is_active:
                continue
            
            is_valid = True
            message = "Consistency check passed"
            error_details = None
            
            try:
                if rule.name == "Donation Date Logic":
                    registration_date = record.get("registration_date")
                    donation_date = record.get("donation_date")
                    
                    if pd.notna(registration_date) and pd.notna(donation_date):
                        if donation_date < registration_date:
                            is_valid = False
                            error_details = {
                                "registration_date": str(registration_date),
                                "donation_date": str(donation_date)
                            }
                
                elif rule.name == "Donation Interval Check":
                    last_donation = record.get("last_donation_date")
                    current_donation = record.get("donation_date")
                    
                    if pd.notna(last_donation) and pd.notna(current_donation):
                        interval_days = (current_donation - last_donation).days
                        if interval_days < 56:
                            is_valid = False
                            error_details = {
                                "interval_days": interval_days,
                                "minimum_required": 56
                            }
                
                if not is_valid:
                    message = f"Consistency rule '{rule.name}' failed: {rule.error_message}"
                    
            except Exception as e:
                is_valid = False
                message = f"Consistency check error: {str(e)}"
                error_details = {"exception": str(e)}
            
            results.append(ValidationResult(
                rule_id=rule.id or "unknown",
                rule_name=rule.name,
                field_name=", ".join(rule.fields_involved),
                record_id=record_id,
                is_valid=is_valid,
                severity=rule.severity,
                message=message,
                error_details=error_details
            ))
        
        return results
    
    def get_quality_metrics(self, validation_results: List[ValidationResult]) -> Dict[str, float]:
        """Calculate data quality metrics"""
        if not validation_results:
            return {"overall_score": 0.0}
        
        total_checks = len(validation_results)
        passed_checks = sum(1 for r in validation_results if r.is_valid)
        
        # Calculate scores by severity
        severity_weights = {
            ValidationSeverity.CRITICAL: 1.0,
            ValidationSeverity.ERROR: 0.8,
            ValidationSeverity.WARNING: 0.5,
            ValidationSeverity.INFO: 0.2
        }
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for result in validation_results:
            weight = severity_weights.get(result.severity, 0.5)
            total_weight += weight
            if result.is_valid:
                weighted_score += weight
        
        overall_score = (weighted_score / total_weight * 100) if total_weight > 0 else 0
        
        return {
            "overall_score": overall_score,
            "completeness_score": self._calculate_completeness(validation_results),
            "accuracy_score": (passed_checks / total_checks) * 100,
            "consistency_score": self._calculate_consistency(validation_results),
            "validity_score": overall_score
        }
    
    def _calculate_completeness(self, results: List[ValidationResult]) -> float:
        """Calculate data completeness score"""
        # This would check for missing required fields
        # Simplified implementation
        return 95.0  # Placeholder
    
    def _calculate_consistency(self, results: List[ValidationResult]) -> float:
        """Calculate data consistency score"""
        consistency_results = [r for r in results if "consistency" in r.rule_name.lower()]
        if not consistency_results:
            return 100.0
        
        passed = sum(1 for r in consistency_results if r.is_valid)
        return (passed / len(consistency_results)) * 100
