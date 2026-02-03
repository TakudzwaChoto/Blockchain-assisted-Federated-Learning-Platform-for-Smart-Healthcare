"""
Donor and donation data models
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum

class BloodType(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class DonationType(str, Enum):
    WHOLE_BLOOD = "whole_blood"
    PLATELETS = "platelets"
    PLASMA = "plasma"
    RED_BLOOD_CELLS = "red_blood_cells"

class DonorCategory(str, Enum):
    INDIVIDUAL = "individual"
    GROUP = "group"
    MILITARY = "military"
    STUDENT = "student"
    HEALTHCARE = "healthcare"
    CIVIL_SERVANT = "civil_servant"

class Donor(BaseModel):
    """Donor information model"""
    id: Optional[str] = None
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=18, le=65)
    gender: str = Field(..., pattern="^(male|female|other)$")
    blood_type: BloodType
    contact_number: str = Field(..., min_length=10, max_length=20)
    email: Optional[str] = Field(None, pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")
    address: Optional[str] = None
    category: DonorCategory = DonorCategory.INDIVIDUAL
    registration_date: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    
    @validator('age')
    def validate_age(cls, v):
        if v < 18 or v > 65:
            raise ValueError('Donor age must be between 18 and 65')
        return v

class Donation(BaseModel):
    """Donation record model"""
    id: Optional[str] = None
    donor_id: str
    donation_date: datetime
    donation_type: DonationType
    volume_ml: float = Field(..., ge=200, le=500)
    location: str
    staff_id: Optional[str] = None
    hemoglobin_level: Optional[float] = Field(None, ge=8.0, le=20.0)
    blood_pressure_systolic: Optional[int] = Field(None, ge=80, le=200)
    blood_pressure_diastolic: Optional[int] = Field(None, ge=50, le=120)
    pulse_rate: Optional[int] = Field(None, ge=40, le=120)
    temperature: Optional[float] = Field(None, ge=35.0, le=42.0)
    notes: Optional[str] = None
    is_successful: bool = True
    
    @validator('volume_ml')
    def validate_volume(cls, v):
        if v < 200 or v > 500:
            raise ValueError('Donation volume must be between 200ml and 500ml')
        return v

class DonorProfile(BaseModel):
    """Comprehensive donor profile for analytics"""
    donor_id: str
    total_donations: int = 0
    total_volume_ml: float = 0.0
    last_donation_date: Optional[datetime] = None
    first_donation_date: Optional[datetime] = None
    average_donation_interval_days: Optional[float] = None
    preferred_donation_type: Optional[DonationType] = None
    donation_frequency_per_year: float = 0.0
    loyalty_score: float = 0.0  # 0-100 scale
    risk_score: float = 0.0  # 0-100 scale
    predicted_next_donation_date: Optional[datetime] = None
    demographic_profile: Dict[str, Any] = Field(default_factory=dict)
    behavioral_patterns: Dict[str, Any] = Field(default_factory=dict)

class BatchDonationData(BaseModel):
    """Model for batch donation data import"""
    donations: List[Donation]
    donors: List[Donor]
    source: str
    import_date: datetime = Field(default_factory=datetime.now)
    total_records: int
    successful_records: int
    failed_records: int
    validation_errors: List[Dict[str, Any]] = Field(default_factory=list)
