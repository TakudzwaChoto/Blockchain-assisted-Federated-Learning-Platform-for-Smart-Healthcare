"""
Pattern mining engine for donor behavior analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from scipy import stats
from mlxtend.frequent_patterns import apriori, association_rules
import warnings
warnings.filterwarnings('ignore')

from ..models.analytics import DonorSegment, DonorBehaviorPattern
from ..config import Config

class PatternMiningEngine:
    """Advanced pattern mining for donor behavior analysis"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)
        self.pattern_cache = {}
        
    def discover_donor_patterns(self, data: pd.DataFrame, 
                              pattern_types: List[str] = None) -> Dict[str, Any]:
        """Discover various donor behavior patterns"""
        if pattern_types is None:
            pattern_types = ["temporal", "behavioral", "demographic", "geographic", "seasonal"]
        
        results = {}
        
        for pattern_type in pattern_types:
            try:
                if pattern_type == "temporal":
                    results["temporal"] = self._mine_temporal_patterns(data)
                elif pattern_type == "behavioral":
                    results["behavioral"] = self._mine_behavioral_patterns(data)
                elif pattern_type == "demographic":
                    results["demographic"] = self._mine_demographic_patterns(data)
                elif pattern_type == "geographic":
                    results["geographic"] = self._mine_geographic_patterns(data)
                elif pattern_type == "seasonal":
                    results["seasonal"] = self._mine_seasonal_patterns(data)
            except Exception as e:
                print(f"Error mining {pattern_type} patterns: {str(e)}")
                results[pattern_type] = {"error": str(e)}
        
        # Generate comprehensive insights
        insights = self._generate_pattern_insights(results)
        results["insights"] = insights
        
        return results
    
    def _mine_temporal_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Mine temporal donation patterns"""
        if "donation_date" not in data.columns:
            return {"error": "donation_date column required"}
        
        # Convert dates
        data["donation_date"] = pd.to_datetime(data["donation_date"])
        
        patterns = {
            "hourly_patterns": self._analyze_hourly_patterns(data),
            "daily_patterns": self._analyze_daily_patterns(data),
            "weekly_patterns": self._analyze_weekly_patterns(data),
            "monthly_patterns": self._analyze_monthly_patterns(data),
            "interval_patterns": self._analyze_interval_patterns(data)
        }
        
        return patterns
    
    def _analyze_hourly_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze hourly donation patterns"""
        data["hour"] = data["donation_date"].dt.hour
        hourly_counts = data.groupby("hour").size()
        
        # Find peak hours
        peak_hours = hourly_counts.nlargest(3).index.tolist()
        low_hours = hourly_counts.nsmallest(3).index.tolist()
        
        return {
            "hourly_distribution": hourly_counts.to_dict(),
            "peak_hours": peak_hours,
            "low_hours": low_hours,
            "peak_percentage": hourly_counts.max() / hourly_counts.sum() * 100,
            "pattern_strength": self._calculate_pattern_strength(hourly_counts.values)
        }
    
    def _analyze_daily_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze daily donation patterns"""
        data["day_of_week"] = data["donation_date"].dt.day_name()
        daily_counts = data.groupby("day_of_week").size()
        
        # Weekend vs weekday analysis
        data["is_weekend"] = data["donation_date"].dt.dayofweek >= 5
        weekend_avg = data[data["is_weekend"]].groupby(data["donation_date"].dt.date).size().mean()
        weekday_avg = data[~data["is_weekend"]].groupby(data["donation_date"].dt.date).size().mean()
        
        return {
            "daily_distribution": daily_counts.to_dict(),
            "weekend_average": weekend_avg,
            "weekday_average": weekday_avg,
            "weekend_vs_weekday_ratio": weekend_avg / weekday_avg if weekday_avg > 0 else 0,
            "busiest_day": daily_counts.idxmax(),
            "slowest_day": daily_counts.idxmin()
        }
    
    def _analyze_weekly_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze weekly donation patterns"""
        data["week"] = data["donation_date"].dt.isocalendar().week
        weekly_counts = data.groupby("week").size()
        
        # Identify trends
        if len(weekly_counts) >= 4:
            trend_slope = self._calculate_trend_slope(weekly_counts.values)
        else:
            trend_slope = 0
        
        return {
            "weekly_distribution": weekly_counts.to_dict(),
            "trend_slope": trend_slope,
            "trend_direction": "increasing" if trend_slope > 0.1 else "decreasing" if trend_slope < -0.1 else "stable",
            "peak_week": weekly_counts.idxmax(),
            "low_week": weekly_counts.idxmin()
        }
    
    def _analyze_monthly_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze monthly donation patterns"""
        data["month"] = data["donation_date"].dt.month
        monthly_counts = data.groupby("month").size()
        
        # Seasonal analysis
        seasons = {
            "winter": [12, 1, 2],
            "spring": [3, 4, 5],
            "summer": [6, 7, 8],
            "fall": [9, 10, 11]
        }
        
        seasonal_counts = {}
        for season, months in seasons.items():
            seasonal_counts[season] = sum(monthly_counts.get(month, 0) for month in months)
        
        return {
            "monthly_distribution": monthly_counts.to_dict(),
            "seasonal_distribution": seasonal_counts,
            "peak_month": monthly_counts.idxmax(),
            "low_month": monthly_counts.idxmin(),
            "seasonal_variation": max(seasonal_counts.values()) / min(seasonal_counts.values()) if min(seasonal_counts.values()) > 0 else 0
        }
    
    def _analyze_interval_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze donation interval patterns"""
        if "donor_id" not in data.columns:
            return {"error": "donor_id column required"}
        
        # Calculate intervals for each donor
        intervals = []
        for donor_id in data["donor_id"].unique():
            donor_data = data[data["donor_id"] == donor_id].sort_values("donation_date")
            if len(donor_data) >= 2:
                donor_intervals = donor_data["donation_date"].diff().dt.days.dropna()
                intervals.extend(donor_intervals.tolist())
        
        if not intervals:
            return {"error": "Insufficient data for interval analysis"}
        
        intervals = np.array(intervals)
        
        return {
            "average_interval": np.mean(intervals),
            "median_interval": np.median(intervals),
            "std_interval": np.std(intervals),
            "interval_distribution": {
                "0-30_days": np.sum(intervals <= 30),
                "31-60_days": np.sum((intervals > 30) & (intervals <= 60)),
                "61-90_days": np.sum((intervals > 60) & (intervals <= 90)),
                "91-180_days": np.sum((intervals > 90) & (intervals <= 180)),
                "180+_days": np.sum(intervals > 180)
            },
            "pattern_consistency": 1 - (np.std(intervals) / np.mean(intervals)) if np.mean(intervals) > 0 else 0
        }
    
    def _mine_behavioral_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Mine behavioral donation patterns"""
        patterns = {
            "volume_patterns": self._analyze_volume_patterns(data),
            "frequency_patterns": self._analyze_frequency_patterns(data),
            "loyalty_patterns": self._analyze_loyalty_patterns(data),
            "drop_risk_patterns": self._analyze_dropout_risk_patterns(data)
        }
        
        return patterns
    
    def _analyze_volume_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze donation volume patterns"""
        if "volume_ml" not in data.columns:
            return {"error": "volume_ml column required"}
        
        volumes = data["volume_ml"].dropna()
        
        # Volume categories
        volume_categories = pd.cut(volumes, bins=[0, 350, 450, 600], labels=["Low", "Standard", "High"])
        volume_dist = volume_categories.value_counts().to_dict()
        
        # Blood type vs volume
        blood_type_volume = {}
        if "blood_type" in data.columns:
            blood_type_volume = data.groupby("blood_type")["volume_ml"].mean().to_dict()
        
        return {
            "volume_statistics": {
                "mean": volumes.mean(),
                "median": volumes.median(),
                "std": volumes.std(),
                "min": volumes.min(),
                "max": volumes.max()
            },
            "volume_distribution": volume_dist,
            "blood_type_averages": blood_type_volume,
            "high_volume_donors_percentage": (volumes >= 450).sum() / len(volumes) * 100
        }
    
    def _analyze_frequency_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze donation frequency patterns"""
        if "donor_id" not in data.columns:
            return {"error": "donor_id column required"}
        
        # Calculate donation frequency per donor
        donor_stats = data.groupby("donor_id").agg({
            "donation_date": ["count", "min", "max"]
        }).reset_index()
        
        donor_stats.columns = ["donor_id", "donation_count", "first_donation", "last_donation"]
        
        # Calculate frequency metrics
        donor_stats["days_active"] = (donor_stats["last_donation"] - donor_stats["first_donation"]).dt.days
        donor_stats["years_active"] = donor_stats["days_active"] / 365.25
        donor_stats["frequency_per_year"] = donor_stats["donation_count"] / donor_stats["years_active"]
        
        # Frequency categories
        frequency_categories = pd.cut(donor_stats["frequency_per_year"], 
                                   bins=[0, 1, 2, 4, float('inf')], 
                                   labels=["Low", "Medium", "High", "Very High"])
        frequency_dist = frequency_categories.value_counts().to_dict()
        
        return {
            "frequency_statistics": {
                "avg_frequency_per_year": donor_stats["frequency_per_year"].mean(),
                "median_frequency_per_year": donor_stats["frequency_per_year"].median(),
                "max_frequency_per_year": donor_stats["frequency_per_year"].max()
            },
            "frequency_distribution": frequency_dist,
            "regular_donors_percentage": (donor_stats["frequency_per_year"] >= 2).sum() / len(donor_stats) * 100
        }
    
    def _analyze_loyalty_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze donor loyalty patterns"""
        if "donor_id" not in data.columns:
            return {"error": "donor_id column required"}
        
        # Calculate loyalty metrics
        donor_stats = data.groupby("donor_id").agg({
            "donation_date": ["count", "min", "max"],
            "volume_ml": "sum"
        }).reset_index()
        
        donor_stats.columns = ["donor_id", "donation_count", "first_donation", "last_donation", "total_volume"]
        
        # Loyalty score calculation
        donor_stats["days_since_last"] = (datetime.now() - donor_stats["last_donation"]).dt.days
        donor_stats["consistency_score"] = self._calculate_consistency_score(data, donor_stats["donor_id"])
        donor_stats["loyalty_score"] = self._calculate_loyalty_score(donor_stats)
        
        # Loyalty segments
        loyalty_segments = pd.cut(donor_stats["loyalty_score"], 
                                bins=[0, 30, 60, 80, 100], 
                                labels=["At Risk", "Occasional", "Regular", "Loyal"])
        loyalty_dist = loyalty_segments.value_counts().to_dict()
        
        return {
            "loyalty_distribution": loyalty_dist,
            "average_loyalty_score": donor_stats["loyalty_score"].mean(),
            "loyal_donors_percentage": (donor_stats["loyalty_score"] >= 80).sum() / len(donor_stats) * 100,
            "at_risk_donors_percentage": (donor_stats["loyalty_score"] < 30).sum() / len(donor_stats) * 100
        }
    
    def _analyze_dropout_risk_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze dropout risk patterns"""
        if "donor_id" not in data.columns:
            return {"error": "donor_id column required"}
        
        # Identify potentially dropped donors
        cutoff_date = datetime.now() - timedelta(days=180)  # 6 months
        recent_donors = set(data[pd.to_datetime(data["donation_date"]) >= cutoff_date]["donor_id"])
        all_donors = set(data["donor_id"].unique())
        dropped_donors = all_donors - recent_donors
        
        # Analyze characteristics of dropped vs active donors
        dropped_data = data[data["donor_id"].isin(dropped_donors)]
        active_data = data[data["donor_id"].isin(recent_donors)]
        
        risk_factors = {}
        
        # Age-based risk
        if "age" in data.columns:
            dropped_avg_age = dropped_data["age"].mean() if not dropped_data.empty else 0
            active_avg_age = active_data["age"].mean() if not active_data.empty else 0
            risk_factors["age_difference"] = dropped_avg_age - active_avg_age
        
        # Volume-based risk
        if "volume_ml" in data.columns:
            dropped_avg_volume = dropped_data["volume_ml"].mean() if not dropped_data.empty else 0
            active_avg_volume = active_data["volume_ml"].mean() if not active_data.empty else 0
            risk_factors["volume_difference"] = dropped_avg_volume - active_avg_volume
        
        # Frequency-based risk
        dropped_freq = self._calculate_average_frequency(dropped_data)
        active_freq = self._calculate_average_frequency(active_data)
        risk_factors["frequency_difference"] = dropped_freq - active_freq
        
        return {
            "total_donors": len(all_donors),
            "active_donors": len(recent_donors),
            "dropped_donors": len(dropped_donors),
            "dropout_rate": len(dropped_donors) / len(all_donors) * 100,
            "risk_factors": risk_factors,
            "high_risk_indicators": self._identify_high_risk_indicators(risk_factors)
        }
    
    def _mine_demographic_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Mine demographic donation patterns"""
        patterns = {
            "age_patterns": self._analyze_age_patterns(data),
            "gender_patterns": self._analyze_gender_patterns(data),
            "blood_type_patterns": self._analyze_blood_type_patterns(data),
            "category_patterns": self._analyze_category_patterns(data)
        }
        
        return patterns
    
    def _analyze_age_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze age-based donation patterns"""
        if "age" not in data.columns:
            return {"error": "age column required"}
        
        # Age groups
        age_groups = pd.cut(data["age"], bins=[0, 25, 35, 45, 55, 65, 100], 
                          labels=["18-25", "26-35", "36-45", "46-55", "56-65", "65+"])
        age_dist = age_groups.value_counts().to_dict()
        
        # Age vs donation metrics
        age_metrics = data.groupby(age_groups).agg({
            "volume_ml": "mean",
            "donor_id": "count" if "donor_id" in data.columns else lambda x: len(x)
        }).to_dict()
        
        return {
            "age_distribution": age_dist,
            "age_metrics": age_metrics,
            "most_active_age_group": max(age_dist, key=age_dist.get),
            "least_active_age_group": min(age_dist, key=age_dist.get)
        }
    
    def _analyze_gender_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze gender-based donation patterns"""
        if "gender" not in data.columns:
            return {"error": "gender column required"}
        
        gender_dist = data["gender"].value_counts().to_dict()
        
        # Gender vs donation metrics
        gender_metrics = data.groupby("gender").agg({
            "volume_ml": "mean",
            "donor_id": "count" if "donor_id" in data.columns else lambda x: len(x)
        }).to_dict()
        
        return {
            "gender_distribution": gender_dist,
            "gender_metrics": gender_metrics,
            "gender_ratio": gender_dist.get("male", 0) / gender_dist.get("female", 1)
        }
    
    def _analyze_blood_type_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze blood type-based donation patterns"""
        if "blood_type" not in data.columns:
            return {"error": "blood_type column required"}
        
        blood_type_dist = data["blood_type"].value_counts().to_dict()
        
        # Blood type vs donation metrics
        blood_type_metrics = data.groupby("blood_type").agg({
            "volume_ml": "mean",
            "donor_id": "count" if "donor_id" in data.columns else lambda x: len(x)
        }).to_dict()
        
        # Calculate demand vs supply ratio (simplified)
        population_blood_type_ratios = {"O+": 37, "O-": 6, "A+": 36, "A-": 6, "B+": 9, "B-": 2, "AB+": 3, "AB-": 1}
        supply_demand_ratios = {}
        
        for blood_type, count in blood_type_dist.items():
            if blood_type in population_blood_type_ratios:
                expected_ratio = population_blood_type_ratios[blood_type] / 100
                actual_ratio = count / sum(blood_type_dist.values())
                supply_demand_ratios[blood_type] = actual_ratio / expected_ratio
        
        return {
            "blood_type_distribution": blood_type_dist,
            "blood_type_metrics": blood_type_metrics,
            "supply_demand_ratios": supply_demand_ratios,
            "most_common_blood_type": max(blood_type_dist, key=blood_type_dist.get),
            "rarest_blood_type": min(blood_type_dist, key=blood_type_dist.get)
        }
    
    def _analyze_category_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze donor category patterns"""
        if "category" not in data.columns:
            return {"error": "category column required"}
        
        category_dist = data["category"].value_counts().to_dict()
        
        # Category vs donation metrics
        category_metrics = data.groupby("category").agg({
            "volume_ml": "mean",
            "donor_id": "count" if "donor_id" in data.columns else lambda x: len(x)
        }).to_dict()
        
        return {
            "category_distribution": category_dist,
            "category_metrics": category_metrics,
            "most_active_category": max(category_dist, key=category_dist.get),
            "category_diversity": len(category_dist)
        }
    
    def _mine_geographic_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Mine geographic donation patterns"""
        if "location" not in data.columns:
            return {"error": "location column required"}
        
        location_dist = data["location"].value_counts().to_dict()
        
        # Location vs donation metrics
        location_metrics = data.groupby("location").agg({
            "volume_ml": "mean",
            "donor_id": "nunique" if "donor_id" in data.columns else lambda x: len(x)
        }).to_dict()
        
        # Regional analysis
        top_locations = list(location_dist.keys())[:5]
        regional_summary = {}
        
        for location in top_locations:
            location_data = data[data["location"] == location]
            regional_summary[location] = {
                "total_donations": len(location_data),
                "unique_donors": location_data["donor_id"].nunique() if "donor_id" in location_data.columns else len(location_data),
                "avg_volume": location_data["volume_ml"].mean() if "volume_ml" in location_data.columns else 0
            }
        
        return {
            "location_distribution": location_dist,
            "location_metrics": location_metrics,
            "top_locations": regional_summary,
            "geographic_diversity": len(location_dist)
        }
    
    def _mine_seasonal_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Mine seasonal donation patterns"""
        if "donation_date" not in data.columns:
            return {"error": "donation_date column required"}
        
        data["donation_date"] = pd.to_datetime(data["donation_date"])
        data["month"] = data["donation_date"].dt.month
        data["quarter"] = data["donation_date"].dt.quarter
        
        # Seasonal distribution
        seasonal_dist = data.groupby("quarter").size().to_dict()
        
        # Month-by-month patterns
        monthly_dist = data.groupby("month").size().to_dict()
        
        # Year-over-year seasonal trends
        data["year"] = data["donation_date"].dt.year
        yoy_seasonal = {}
        
        for year in data["year"].unique():
            year_data = data[data["year"] == year]
            yoy_seasonal[year] = year_data.groupby("quarter").size().to_dict()
        
        return {
            "seasonal_distribution": seasonal_dist,
            "monthly_distribution": monthly_dist,
            "year_over_year_seasonal": yoy_seasonal,
            "peak_season": max(seasonal_dist, key=seasonal_dist.get),
            "low_season": min(seasonal_dist, key=seasonal_dist.get),
            "seasonal_variation": max(seasonal_dist.values()) / min(seasonal_dist.values()) if min(seasonal_dist.values()) > 0 else 0
        }
    
    def _calculate_pattern_strength(self, values: np.ndarray) -> float:
        """Calculate pattern strength (0-1 scale)"""
        if len(values) < 2:
            return 0.0
        
        # Use coefficient of variation as pattern strength indicator
        cv = np.std(values) / np.mean(values) if np.mean(values) > 0 else 0
        strength = 1 - min(cv, 1.0)  # Lower variation = stronger pattern
        
        return strength
    
    def _calculate_trend_slope(self, values: np.ndarray) -> float:
        """Calculate trend slope using linear regression"""
        if len(values) < 2:
            return 0.0
        
        x = np.arange(len(values))
        slope, _, _, _, _ = stats.linregress(x, values)
        
        return slope
    
    def _calculate_consistency_score(self, data: pd.DataFrame, donor_ids: pd.Series) -> pd.Series:
        """Calculate donation consistency score for donors"""
        consistency_scores = []
        
        for donor_id in donor_ids:
            donor_data = data[data["donor_id"] == donor_id].sort_values("donation_date")
            if len(donor_data) >= 2:
                intervals = donor_data["donation_date"].diff().dt.days.dropna()
                consistency = 1 - (np.std(intervals) / np.mean(intervals)) if np.mean(intervals) > 0 else 0
                consistency_scores.append(min(consistency, 1.0))
            else:
                consistency_scores.append(0.5)  # Neutral score for single donations
        
        return pd.Series(consistency_scores, index=donor_ids)
    
    def _calculate_loyalty_score(self, donor_stats: pd.DataFrame) -> pd.Series:
        """Calculate comprehensive loyalty score"""
        # Factors: frequency, recency, volume, consistency
        freq_score = np.clip(donor_stats["donation_count"] / 10, 0, 1) * 25
        recency_score = np.clip(1 - (donor_stats["days_since_last"] / 365), 0, 1) * 25
        volume_score = np.clip(donor_stats["total_volume"] / 2000, 0, 1) * 25
        consistency_score = donor_stats["consistency_score"] * 25
        
        loyalty_score = freq_score + recency_score + volume_score + consistency_score
        
        return loyalty_score
    
    def _calculate_average_frequency(self, data: pd.DataFrame) -> float:
        """Calculate average donation frequency for a dataset"""
        if "donor_id" not in data.columns or len(data) == 0:
            return 0.0
        
        donor_stats = data.groupby("donor_id").agg({
            "donation_date": ["count", "min", "max"]
        }).reset_index()
        
        donor_stats.columns = ["donor_id", "donation_count", "first_donation", "last_donation"]
        donor_stats["years_active"] = (donor_stats["last_donation"] - donor_stats["first_donation"]).dt.days / 365.25
        donor_stats["frequency_per_year"] = donor_stats["donation_count"] / donor_stats["years_active"]
        
        return donor_stats["frequency_per_year"].mean()
    
    def _identify_high_risk_indicators(self, risk_factors: Dict[str, float]) -> List[str]:
        """Identify high-risk indicators from risk factor analysis"""
        indicators = []
        
        if risk_factors.get("age_difference", 0) > 5:
            indicators.append("Older donors more likely to drop out")
        
        if risk_factors.get("volume_difference", 0) < -20:
            indicators.append("Lower donation volume associated with dropout")
        
        if risk_factors.get("frequency_difference", 0) < -0.5:
            indicators.append("Lower donation frequency predicts dropout")
        
        return indicators
    
    def _generate_pattern_insights(self, pattern_results: Dict[str, Any]) -> List[str]:
        """Generate comprehensive insights from pattern analysis"""
        insights = []
        
        # Temporal insights
        if "temporal" in pattern_results and "error" not in pattern_results["temporal"]:
            temporal = pattern_results["temporal"]
            
            if "weekly_patterns" in temporal:
                weekend_ratio = temporal["weekly_patterns"].get("weekend_vs_weekday_ratio", 1)
                if weekend_ratio > 1.2:
                    insights.append("Weekend donations significantly higher than weekdays")
                elif weekend_ratio < 0.8:
                    insights.append("Weekday donations significantly higher than weekends")
            
            if "monthly_patterns" in temporal:
                seasonal_var = temporal["monthly_patterns"].get("seasonal_variation", 1)
                if seasonal_var > 2:
                    insights.append("Strong seasonal variation in donation patterns")
        
        # Behavioral insights
        if "behavioral" in pattern_results and "error" not in pattern_results["behavioral"]:
            behavioral = pattern_results["behavioral"]
            
            if "loyalty_patterns" in behavioral:
                loyal_pct = behavioral["loyalty_patterns"].get("loyal_donors_percentage", 0)
                if loyal_pct < 20:
                    insights.append("Low donor loyalty - retention programs needed")
                elif loyal_pct > 50:
                    insights.append("High donor loyalty - maintain current engagement strategies")
            
            if "drop_risk_patterns" in behavioral:
                dropout_rate = behavioral["drop_risk_patterns"].get("dropout_rate", 0)
                if dropout_rate > 30:
                    insights.append("High dropout rate - immediate intervention required")
        
        # Demographic insights
        if "demographic" in pattern_results and "error" not in pattern_results["demographic"]:
            demographic = pattern_results["demographic"]
            
            if "blood_type_patterns" in demographic:
                supply_demand = demographic["blood_type_patterns"].get("supply_demand_ratios", {})
                critical_types = [bt for bt, ratio in supply_demand.items() if ratio < 0.8]
                if critical_types:
                    insights.append(f"Critical shortage of {', '.join(critical_types)} blood types")
        
        # Geographic insights
        if "geographic" in pattern_results and "error" not in pattern_results["geographic"]:
            geographic = pattern_results["geographic"]
            diversity = geographic.get("geographic_diversity", 0)
            if diversity < 5:
                insights.append("Limited geographic diversity - expansion opportunities")
            elif diversity > 20:
                insights.append("High geographic diversity - optimize regional strategies")
        
        if not insights:
            insights.append("Pattern analysis completed - review detailed results for specific insights")
        
        return insights
    
    def create_donor_segments_from_patterns(self, data: pd.DataFrame, 
                                          pattern_results: Dict[str, Any]) -> List[DonorSegment]:
        """Create donor segments based on discovered patterns"""
        segments = []
        
        # Create segments based on behavioral patterns
        if "behavioral" in pattern_results and "error" not in pattern_results["behavioral"]:
            behavioral = pattern_results["behavioral"]
            
            # High-frequency loyal donors
            if "loyalty_patterns" in behavioral:
                segments.append(DonorSegment(
                    segment_name="High-Frequency Loyal Donors",
                    algorithm="pattern_mining",
                    segment_size=0,  # Would be calculated from actual data
                    percentage_of_total=0,
                    characteristics={"frequency": "high", "loyalty": "high"},
                    avg_donation_frequency=4.0,
                    avg_donation_volume=450,
                    loyalty_score_avg=85,
                    risk_score_avg=15,
                    recommended_actions=["Priority booking", "Special recognition programs"]
                ))
            
            # At-risk donors
            if "drop_risk_patterns" in behavioral:
                segments.append(DonorSegment(
                    segment_name="At-Risk Donors",
                    algorithm="pattern_mining",
                    segment_size=0,
                    percentage_of_total=0,
                    characteristics={"dropout_risk": "high"},
                    avg_donation_frequency=1.0,
                    avg_donation_volume=350,
                    loyalty_score_avg=25,
                    risk_score_avg=75,
                    recommended_actions=["Re-engagement campaigns", "Personalized outreach"]
                ))
        
        # Create segments based on demographic patterns
        if "demographic" in pattern_results and "error" not in pattern_results["demographic"]:
            demographic = pattern_results["demographic"]
            
            if "age_patterns" in demographic:
                segments.append(DonorSegment(
                    segment_name="Young Adult Donors (18-25)",
                    algorithm="pattern_mining",
                    segment_size=0,
                    percentage_of_total=0,
                    characteristics={"age_group": "18-25"},
                    avg_donation_frequency=2.0,
                    avg_donation_volume=400,
                    loyalty_score_avg=60,
                    risk_score_avg=40,
                    recommended_actions=["Campus outreach", "Social media campaigns"]
                ))
        
        return segments
