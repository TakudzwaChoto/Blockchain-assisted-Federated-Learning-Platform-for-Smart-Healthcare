"""
Analytics and forecasting models
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any, Tuple
from pydantic import BaseModel, Field
from enum import Enum

class TimeGranularity(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class AnalysisDimension(str, Enum):
    TIME = "time"
    REGION = "region"
    AGE_GROUP = "age_group"
    GENDER = "gender"
    DONATION_TYPE = "donation_type"
    DONOR_CATEGORY = "donor_category"
    BLOOD_TYPE = "blood_type"

class BloodTrend(BaseModel):
    """Blood donation trend analysis model"""
    id: Optional[str] = None
    analysis_date: datetime = Field(default_factory=datetime.now)
    time_period: str
    granularity: TimeGranularity
    dimension: AnalysisDimension
    metric: str  # e.g., "donation_volume", "donor_count", "donation_frequency"
    values: List[Dict[str, Any]]  # Time series data
    trend_direction: str  # "increasing", "decreasing", "stable"
    trend_percentage: float
    year_over_year_change: Optional[float] = None
    month_over_month_change: Optional[float] = None
    statistical_significance: float
    confidence_interval: Tuple[float, float]
    insights: List[str] = Field(default_factory=list)
    
class DemandForecast(BaseModel):
    """Blood demand forecast model"""
    id: Optional[str] = None
    forecast_date: datetime = Field(default_factory=datetime.now)
    model_type: str  # "arima", "prophet", "lstm", "linear_regression"
    target_variable: str  # e.g., "blood_demand", "donation_volume"
    forecast_horizon_days: int
    granularity: TimeGranularity
    training_data_period_days: int
    forecast_values: List[Dict[str, Any]]
    confidence_intervals: List[Tuple[float, float]]
    model_performance: Dict[str, float]  # R², RMSE, MAPE
    feature_importance: Optional[Dict[str, float]] = None
    last_training_date: datetime
    next_training_date: Optional[datetime] = None
    accuracy_score: float
    is_active: bool = True

class DonorSegment(BaseModel):
    """Donor segmentation model"""
    id: Optional[str] = None
    segment_name: str
    algorithm: str  # "kmeans", "dbscan", "hierarchical"
    creation_date: datetime = Field(default_factory=datetime.now)
    segment_size: int
    percentage_of_total: float
    characteristics: Dict[str, Any]
    avg_donation_frequency: float
    avg_donation_volume: float
    loyalty_score_avg: float
    risk_score_avg: float
    predicted_churn_probability: Optional[float] = None
    recommended_actions: List[str] = Field(default_factory=list)
    
class DonorBehaviorPattern(BaseModel):
    """Donor behavioral pattern analysis"""
    id: Optional[str] = None
    pattern_type: str  # "frequent_donor", "seasonal_donor", "irregular_donor"
    donor_count: int
    pattern_description: str
    key_indicators: List[str]
    avg_donation_interval: Optional[float] = None
    seasonal_trends: Optional[Dict[str, float]] = None
    risk_factors: List[str] = Field(default_factory=list)
    retention_probability: Optional[float] = None
    
class RecommendationEngine(BaseModel):
    """Intelligent recommendation model"""
    id: Optional[str] = None
    recommendation_type: str  # "donor_recall", "inventory_optimization", "campaign_targeting"
    target_audience: str
    recommendation_date: datetime = Field(default_factory=datetime.now)
    priority_score: float  # 0-100
    expected_impact: Dict[str, float]
    action_items: List[str]
    success_probability: float
    cost_estimate: Optional[float] = None
    implementation_timeline: Optional[str] = None
    
class QualityAlert(BaseModel):
    """Data quality and business rule alerts"""
    id: Optional[str] = None
    alert_type: str  # "data_quality", "business_rule", "anomaly_detection"
    severity: str  # "low", "medium", "high", "critical"
    message: str
    affected_records: int
    detection_date: datetime = Field(default_factory=datetime.now)
    resolution_status: str = "open"  # "open", "in_progress", "resolved"
    recommended_action: Optional[str] = None
    auto_resolvable: bool = False
