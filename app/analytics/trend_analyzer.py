"""
Blood donation trend analysis engine
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

from ..models.analytics import BloodTrend, AnalysisDimension, TimeGranularity
from ..config import Config

class TrendAnalyzer:
    """Comprehensive trend analysis for blood donation data"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # Keep 95% variance
        
    def analyze_donation_trends(self, data: pd.DataFrame, 
                              dimensions: List[str] = None,
                              time_granularity: str = "monthly",
                              time_period_days: int = 365) -> Dict[str, BloodTrend]:
        """Analyze blood donation trends across multiple dimensions"""
        if dimensions is None:
            dimensions = ["time", "region", "age_group", "gender", "blood_type", "donation_type"]
        
        results = {}
        
        # Ensure data has required date column
        if "donation_date" not in data.columns:
            raise ValueError("Data must contain 'donation_date' column")
        
        # Convert dates and filter by time period
        data["donation_date"] = pd.to_datetime(data["donation_date"])
        cutoff_date = datetime.now() - timedelta(days=time_period_days)
        filtered_data = data[data["donation_date"] >= cutoff_date].copy()
        
        for dimension in dimensions:
            try:
                trend = self._analyze_dimension_trend(filtered_data, dimension, time_granularity)
                results[dimension] = trend
            except Exception as e:
                print(f"Error analyzing {dimension} trend: {str(e)}")
                continue
        
        return results
    
    def _analyze_dimension_trend(self, data: pd.DataFrame, dimension: str, 
                               granularity: str) -> BloodTrend:
        """Analyze trend for a specific dimension"""
        # Prepare time-based aggregation
        time_col = self._get_time_column(data, granularity)
        
        # Group by time and dimension
        if dimension == "time":
            grouped_data = self._group_by_time(data, time_col)
        else:
            grouped_data = data.groupby([time_col, dimension]).agg({
                "volume_ml": ["sum", "count", "mean"],
                "donor_id": "nunique" if "donor_id" in data.columns else lambda x: len(x)
            }).reset_index()
        
        # Calculate trend metrics
        trend_metrics = self._calculate_trend_metrics(grouped_data, dimension)
        
        # Generate insights
        insights = self._generate_trend_insights(grouped_data, dimension, trend_metrics)
        
        return BloodTrend(
            analysis_date=datetime.now(),
            time_period=f"Last {len(grouped_data)} {granularity} periods",
            granularity=TimeGranularity(granularity),
            dimension=AnalysisDimension(dimension),
            metric="donation_volume",
            values=self._format_trend_values(grouped_data),
            trend_direction=trend_metrics["direction"],
            trend_percentage=trend_metrics["percentage"],
            year_over_year_change=trend_metrics.get("yoy_change"),
            month_over_month_change=trend_metrics.get("mom_change"),
            statistical_significance=trend_metrics["significance"],
            confidence_interval=trend_metrics["confidence_interval"],
            insights=insights
        )
    
    def _get_time_column(self, data: pd.DataFrame, granularity: str) -> str:
        """Get appropriate time column based on granularity"""
        if granularity == "daily":
            return data["donation_date"].dt.date.astype(str)
        elif granularity == "weekly":
            return data["donation_date"].dt.to_period('W').astype(str)
        elif granularity == "monthly":
            return data["donation_date"].dt.to_period('M').astype(str)
        elif granularity == "quarterly":
            return data["donation_date"].dt.to_period('Q').astype(str)
        elif granularity == "yearly":
            return data["donation_date"].dt.to_period('Y').astype(str)
        else:
            return data["donation_date"].dt.to_period('M').astype(str)
    
    def _group_by_time(self, data: pd.DataFrame, time_col: pd.Series) -> pd.DataFrame:
        """Group data by time periods"""
        return data.groupby(time_col).agg({
            "volume_ml": ["sum", "count", "mean"],
            "donor_id": "nunique" if "donor_id" in data.columns else lambda x: len(x)
        }).reset_index()
    
    def _calculate_trend_metrics(self, data: pd.DataFrame, dimension: str) -> Dict[str, Any]:
        """Calculate trend statistics"""
        # Extract volume values
        if "volume_ml" in data.columns:
            if isinstance(data["volume_ml"], pd.DataFrame):
                volumes = data["volume_ml"]["sum"].values
            else:
                volumes = data["volume_ml"].values
        else:
            volumes = np.zeros(len(data))
        
        if len(volumes) < 2:
            return {
                "direction": "stable",
                "percentage": 0.0,
                "significance": 0.0,
                "confidence_interval": (0.0, 0.0)
            }
        
        # Linear regression for trend
        x = np.arange(len(volumes))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, volumes)
        
        # Calculate trend direction and percentage
        if slope > 0:
            direction = "increasing"
        elif slope < 0:
            direction = "decreasing"
        else:
            direction = "stable"
        
        # Calculate percentage change
        if volumes[0] != 0:
            percentage_change = ((volumes[-1] - volumes[0]) / volumes[0]) * 100
        else:
            percentage_change = 0.0
        
        # Calculate confidence interval
        confidence_interval = self._calculate_confidence_interval(volumes, slope, std_err)
        
        # Calculate YoY and MoM changes if enough data
        yoy_change = None
        mom_change = None
        
        if len(volumes) >= 12:  # Year-over-year
            yoy_change = ((volumes[-1] - volumes[-12]) / volumes[-12]) * 100 if volumes[-12] != 0 else None
        
        if len(volumes) >= 2:  # Month-over-month
            mom_change = ((volumes[-1] - volumes[-2]) / volumes[-2]) * 100 if volumes[-2] != 0 else None
        
        return {
            "direction": direction,
            "percentage": percentage_change,
            "significance": p_value,
            "confidence_interval": confidence_interval,
            "yoy_change": yoy_change,
            "mom_change": mom_change,
            "slope": slope,
            "r_squared": r_value ** 2
        }
    
    def _calculate_confidence_interval(self, values: np.ndarray, slope: float, 
                                     std_err: float) -> Tuple[float, float]:
        """Calculate confidence interval for trend"""
        n = len(values)
        if n < 3:
            return (0.0, 0.0)
        
        # 95% confidence interval
        t_critical = stats.t.ppf(0.975, n - 2)
        margin_error = t_critical * std_err
        
        # Convert to percentage change
        if values[0] != 0:
            lower_bound = ((values[0] + slope * (n - 1) - margin_error) / values[0] - 1) * 100
            upper_bound = ((values[0] + slope * (n - 1) + margin_error) / values[0] - 1) * 100
        else:
            lower_bound = -margin_error
            upper_bound = margin_error
        
        return (lower_bound, upper_bound)
    
    def _generate_trend_insights(self, data: pd.DataFrame, dimension: str, 
                                trend_metrics: Dict[str, Any]) -> List[str]:
        """Generate insights based on trend analysis"""
        insights = []
        
        direction = trend_metrics["direction"]
        percentage = trend_metrics["percentage"]
        significance = trend_metrics["significance"]
        
        # Trend direction insights
        if direction == "increasing":
            if percentage > 10:
                insights.append(f"Strong upward trend in {dimension} with {percentage:.1f}% increase")
            else:
                insights.append(f"Moderate increase in {dimension} of {percentage:.1f}%")
        elif direction == "decreasing":
            if percentage < -10:
                insights.append(f"Concerning downward trend in {dimension} with {percentage:.1f}% decrease")
            else:
                insights.append(f"Slight decrease in {dimension} of {percentage:.1f}%")
        else:
            insights.append(f"Stable trend in {dimension}")
        
        # Statistical significance
        if significance < 0.05:
            insights.append(f"Trend is statistically significant (p={significance:.3f})")
        else:
            insights.append(f"Trend is not statistically significant (p={significance:.3f})")
        
        # Seasonal patterns
        seasonal_insight = self._detect_seasonal_patterns(data)
        if seasonal_insight:
            insights.append(seasonal_insight)
        
        # Dimension-specific insights
        dimension_insight = self._get_dimension_specific_insights(data, dimension)
        if dimension_insight:
            insights.extend(dimension_insight)
        
        return insights
    
    def _detect_seasonal_patterns(self, data: pd.DataFrame) -> Optional[str]:
        """Detect seasonal patterns in the data"""
        if len(data) < 12:  # Need at least 12 periods for seasonal analysis
            return None
        
        # Extract volume values
        if "volume_ml" in data.columns:
            if isinstance(data["volume_ml"], pd.DataFrame):
                volumes = data["volume_ml"]["sum"].values
            else:
                volumes = data["volume_ml"].values
        else:
            return None
        
        # Simple seasonal detection using autocorrelation
        if len(volumes) >= 12:
            # Check for yearly pattern (12 periods)
            autocorr_12 = np.corrcoef(volumes[:-12], volumes[12:])[0, 1] if len(volumes) > 12 else 0
            
            if autocorr_12 > 0.5:
                return "Strong seasonal pattern detected with yearly cycle"
            elif autocorr_12 > 0.3:
                return "Moderate seasonal pattern detected"
        
        return None
    
    def _get_dimension_specific_insights(self, data: pd.DataFrame, dimension: str) -> List[str]:
        """Generate dimension-specific insights"""
        insights = []
        
        if dimension == "blood_type" and "blood_type" in data.columns:
            # Find most and least common blood types
            blood_type_counts = data.groupby("blood_type")["volume_ml"].sum() if "volume_ml" in data.columns else data.groupby("blood_type").size()
            if not blood_type_counts.empty:
                most_common = blood_type_counts.idxmax()
                least_common = blood_type_counts.idxmin()
                insights.append(f"Most common blood type: {most_common}")
                insights.append(f"Least common blood type: {least_common}")
        
        elif dimension == "age_group" and "age_group" in data.columns:
            # Age group analysis
            age_group_counts = data.groupby("age_group")["volume_ml"].sum() if "volume_ml" in data.columns else data.groupby("age_group").size()
            if not age_group_counts.empty:
                top_age_group = age_group_counts.idxmax()
                insights.append(f"Most active age group: {top_age_group}")
        
        elif dimension == "gender" and "gender" in data.columns:
            # Gender distribution
            gender_counts = data.groupby("gender")["volume_ml"].sum() if "volume_ml" in data.columns else data.groupby("gender").size()
            if not gender_counts.empty:
                insights.append(f"Gender distribution: {dict(gender_counts)}")
        
        elif dimension == "donation_type" and "donation_type" in data.columns:
            # Donation type analysis
            type_counts = data.groupby("donation_type")["volume_ml"].sum() if "volume_ml" in data.columns else data.groupby("donation_type").size()
            if not type_counts.empty:
                popular_type = type_counts.idxmax()
                insights.append(f"Most popular donation type: {popular_type}")
        
        return insights
    
    def _format_trend_values(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Format trend values for output"""
        values = []
        
        # Handle different data structures
        if isinstance(data.index, pd.RangeIndex):
            # Simple time series
            for i, row in data.iterrows():
                if "volume_ml" in data.columns:
                    if isinstance(data["volume_ml"], pd.DataFrame):
                        volume = row["volume_ml"]["sum"] if not pd.isna(row["volume_ml"]["sum"]) else 0
                        count = row["volume_ml"]["count"] if not pd.isna(row["volume_ml"]["count"]) else 0
                    else:
                        volume = row["volume_ml"] if not pd.isna(row["volume_ml"]) else 0
                        count = 1
                else:
                    volume = 0
                    count = 0
                
                values.append({
                    "period": str(i),
                    "volume": volume,
                    "count": count,
                    "donors": row.get("donor_id", 0) if not pd.isna(row.get("donor_id", 0)) else 0
                })
        else:
            # Multi-dimensional data
            for i, row in data.iterrows():
                if "volume_ml" in data.columns:
                    if isinstance(data["volume_ml"], pd.DataFrame):
                        volume = row["volume_ml"]["sum"] if not pd.isna(row["volume_ml"]["sum"]) else 0
                        count = row["volume_ml"]["count"] if not pd.isna(row["volume_ml"]["count"]) else 0
                    else:
                        volume = row["volume_ml"] if not pd.isna(row["volume_ml"]) else 0
                        count = 1
                else:
                    volume = 0
                    count = 0
                
                values.append({
                    "period": str(row.iloc[0]),  # First column is usually time
                    "dimension": str(row.iloc[1]) if len(row) > 1 else "unknown",
                    "volume": volume,
                    "count": count,
                    "donors": row.get("donor_id", 0) if not pd.isna(row.get("donor_id", 0)) else 0
                })
        
        return values
    
    def generate_donor_profiles(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive donor profiles for active donor groups"""
        if "donor_id" not in data.columns:
            return {"error": "donor_id column required for donor profiling"}
        
        # Aggregate donor data
        donor_profiles = data.groupby("donor_id").agg({
            "volume_ml": ["sum", "mean", "count"],
            "donation_date": ["min", "max"],
            "blood_type": "first",
            "age": "first",
            "gender": "first",
            "category": "first" if "category" in data.columns else lambda x: "individual"
        }).reset_index()
        
        # Flatten column names
        donor_profiles.columns = ['donor_id', 'total_volume', 'avg_volume', 'donation_count', 
                                'first_donation', 'last_donation', 'blood_type', 'age', 'gender', 'category']
        
        # Calculate additional metrics
        donor_profiles["days_between_donations"] = (
            (donor_profiles["last_donation"] - donor_profiles["first_donation"]).dt.days / 
            (donor_profiles["donation_count"] - 1)
        ).fillna(0)
        
        donor_profiles["donation_frequency_per_year"] = (
            donor_profiles["donation_count"] / 
            ((datetime.now() - donor_profiles["first_donation"]).dt.days / 365.25)
        ).fillna(0)
        
        # Categorize donors
        donor_profiles["donor_category"] = donor_profiles.apply(self._categorize_donor, axis=1)
        
        # Generate group profiles
        group_profiles = {}
        for category in ["military", "student", "healthcare", "civil_servant"]:
            if category in donor_profiles["category"].values:
                category_data = donor_profiles[donor_profiles["category"] == category]
                group_profiles[category] = {
                    "count": len(category_data),
                    "avg_age": category_data["age"].mean(),
                    "avg_volume_per_year": category_data["donation_frequency_per_year"].mean() * category_data["avg_volume"].mean(),
                    "most_common_blood_type": category_data["blood_type"].mode().iloc[0] if not category_data["blood_type"].mode().empty else "Unknown",
                    "gender_distribution": category_data["gender"].value_counts().to_dict(),
                    "avg_donation_interval_days": category_data["days_between_donations"].mean()
                }
        
        return {
            "total_donors": len(donor_profiles),
            "donor_categories": donor_profiles["donor_category"].value_counts().to_dict(),
            "group_profiles": group_profiles,
            "top_donors": donor_profiles.nlargest(10, "total_volume")[["donor_id", "total_volume", "donation_count"]].to_dict("records"),
            "profile_summary": {
                "avg_donor_age": donor_profiles["age"].mean(),
                "avg_donations_per_donor": donor_profiles["donation_count"].mean(),
                "avg_volume_per_donor": donor_profiles["total_volume"].mean(),
                "most_active_category": donor_profiles["category"].mode().iloc[0] if not donor_profiles["category"].mode().empty else "individual"
            }
        }
    
    def _categorize_donor(self, donor_row: pd.Series) -> str:
        """Categorize donor based on donation patterns"""
        donation_count = donor_row["donation_count"]
        frequency = donor_row["donation_frequency_per_year"]
        
        if donation_count >= 10 and frequency >= 3:
            return "frequent_donor"
        elif donation_count >= 5 and frequency >= 2:
            return "regular_donor"
        elif donation_count >= 2:
            return "occasional_donor"
        else:
            return "new_donor"
