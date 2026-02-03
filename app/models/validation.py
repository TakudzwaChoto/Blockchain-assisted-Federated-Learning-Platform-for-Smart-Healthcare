"""
Data validation and rule management models
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum

class RuleType(str, Enum):
    DATA_TYPE = "data_type"
    RANGE_CHECK = "range_check"
    FORMAT_VALIDATION = "format_validation"
    BUSINESS_RULE = "business_rule"
    CONSISTENCY_CHECK = "consistency_check"
    REFERENCE_CHECK = "reference_check"

class ValidationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class DataRule(BaseModel):
    """Data validation rule model"""
    id: Optional[str] = None
    name: str
    description: str
    rule_type: RuleType
    field_name: str
    condition: Optional[str] = None  # SQL-like condition or expression
    expected_value: Optional[Union[str, int, float, bool, List]] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    allowed_values: Optional[List[Union[str, int, float]]] = None
    pattern: Optional[str] = None  # Regex pattern
    severity: ValidationSeverity = ValidationSeverity.ERROR
    is_active: bool = True
    created_date: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    created_by: Optional[str] = None
    
class ValidationResult(BaseModel):
    """Validation result model"""
    rule_id: str
    rule_name: str
    field_name: str
    record_id: Optional[str] = None
    actual_value: Optional[Union[str, int, float, bool]] = None
    expected_value: Optional[Union[str, int, float, bool, List]] = None
    is_valid: bool
    severity: ValidationSeverity
    message: str
    error_details: Optional[Dict[str, Any]] = None
    validation_date: datetime = Field(default_factory=datetime.now)

class BatchValidationResult(BaseModel):
    """Batch validation results"""
    batch_id: str
    total_records: int
    valid_records: int
    invalid_records: int
    validation_results: List[ValidationResult]
    summary_by_severity: Dict[str, int] = Field(default_factory=dict)
    summary_by_rule: Dict[str, Dict[str, int]] = Field(default_factory=dict)
    processing_time_seconds: float
    validation_date: datetime = Field(default_factory=datetime.now)

class DataQualityMetrics(BaseModel):
    """Data quality metrics dashboard"""
    measurement_date: datetime = Field(default_factory=datetime.now)
    total_records: int
    completeness_score: float  # 0-100
    accuracy_score: float  # 0-100
    consistency_score: float  # 0-100
    validity_score: float  # 0-100
    timeliness_score: float  # 0-100
    overall_quality_score: float  # 0-100
    field_quality_scores: Dict[str, float] = Field(default_factory=dict)
    quality_trends: List[Dict[str, Any]] = Field(default_factory=list)
    
class ConsistencyRule(BaseModel):
    """Cross-field consistency rules"""
    id: Optional[str] = None
    name: str
    description: str
    fields_involved: List[str]
    rule_expression: str  # Logical expression
    error_message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    is_active: bool = True
    created_date: datetime = Field(default_factory=datetime.now)

class BusinessRule(BaseModel):
    """Business logic validation rules"""
    id: Optional[str] = None
    name: str
    description: str
    domain: str  # "donation", "donor", "inventory", "testing"
    rule_logic: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    error_message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    is_active: bool = True
    created_date: datetime = Field(default_factory=datetime.now)
    
# Predefined blood domain validation rules
BLOOD_DOMAIN_RULES = [
    DataRule(
        name="Blood Type Validation",
        description="Validates blood type format and values",
        rule_type=RuleType.FORMAT_VALIDATION,
        field_name="blood_type",
        allowed_values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        severity=ValidationSeverity.ERROR
    ),
    DataRule(
        name="Donor Age Range",
        description="Validates donor age is within acceptable range",
        rule_type=RuleType.RANGE_CHECK,
        field_name="age",
        min_value=18,
        max_value=65,
        severity=ValidationSeverity.ERROR
    ),
    DataRule(
        name="Donation Volume Range",
        description="Validates donation volume is within standard range",
        rule_type=RuleType.RANGE_CHECK,
        field_name="volume_ml",
        min_value=200,
        max_value=500,
        severity=ValidationSeverity.ERROR
    ),
    DataRule(
        name="Hemoglobin Level",
        description="Validates hemoglobin level is within healthy range",
        rule_type=RuleType.RANGE_CHECK,
        field_name="hemoglobin_level",
        min_value=8.0,
        max_value=20.0,
        severity=ValidationSeverity.WARNING
    ),
    DataRule(
        name="Email Format",
        description="Validates email format if provided",
        rule_type=RuleType.FORMAT_VALIDATION,
        field_name="email",
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        severity=ValidationSeverity.WARNING
    )
]

# Consistency rules for blood domain
BLOOD_CONSISTENCY_RULES = [
    ConsistencyRule(
        name="Donation Date Logic",
        description="Donation date cannot be before donor registration date",
        fields_involved=["donation_date", "registration_date"],
        rule_expression="donation_date >= registration_date",
        error_message="Donation date cannot be earlier than donor registration date"
    ),
    ConsistencyRule(
        name="Donation Interval Check",
        description="Minimum 56 days between whole blood donations",
        fields_involved=["donation_date", "last_donation_date"],
        rule_expression="donation_date - last_donation_date >= 56 days OR last_donation_date IS NULL",
        error_message="Minimum 56 days required between whole blood donations"
    )
]
