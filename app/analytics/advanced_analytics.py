"""
Advanced analytics and intelligent decision support
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from sklearn.cluster import KMeans, DBSCAN
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from scipy.stats import pearsonr
from mlxtend.frequent_patterns import apriori, association_rules
import warnings
warnings.filterwarnings('ignore')

from ..models.analytics import DonorSegment, DonorBehaviorPattern, RecommendationEngine, QualityAlert
from ..config import Config

class AdvancedAnalytics:
    """Advanced analytics engine for blood domain intelligence"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.trained_models = {}
        
    def perform_clustering_analysis(self, data: pd.DataFrame, 
                                  algorithm: str = "kmeans",
                                  features: List[str] = None,
                                  n_clusters: int = 5) -> Dict[str, Any]:
        """Perform donor segmentation using clustering algorithms"""
        if features is None:
            features = self._get_default_clustering_features(data)
        
        # Prepare data
        prepared_data = self._prepare_clustering_data(data, features)
        
        if algorithm == "kmeans":
            clusters, model = self._kmeans_clustering(prepared_data, n_clusters)
        elif algorithm == "dbscan":
            clusters, model = self._dbscan_clustering(prepared_data)
        else:
            raise ValueError(f"Unsupported clustering algorithm: {algorithm}")
        
        # Analyze clusters
        cluster_analysis = self._analyze_clusters(data, clusters, features)
        
        # Create donor segments
        segments = self._create_donor_segments(data, clusters, algorithm, cluster_analysis)
        
        return {
            "algorithm": algorithm,
            "n_clusters": len(np.unique(clusters)),
            "cluster_labels": clusters.tolist(),
            "cluster_analysis": cluster_analysis,
            "segments": segments,
            "model_info": self._get_model_info(model, algorithm)
        }
    
    def _get_default_clustering_features(self, data: pd.DataFrame) -> List[str]:
        """Get default features for clustering"""
        available_features = []
        
        potential_features = [
            "age", "volume_ml", "donation_frequency_per_year", "days_between_donations",
            "eligibility_score", "total_donations", "avg_donation_interval_days"
        ]
        
        for feature in potential_features:
            if feature in data.columns:
                available_features.append(feature)
        
        return available_features
    
    def _prepare_clustering_data(self, data: pd.DataFrame, features: List[str]) -> np.ndarray:
        """Prepare and scale data for clustering"""
        # Extract features
        clustering_data = data[features].copy()
        
        # Handle missing values
        clustering_data = clustering_data.fillna(clustering_data.mean())
        
        # Scale features
        scaled_data = self.scaler.fit_transform(clustering_data)
        
        return scaled_data
    
    def _kmeans_clustering(self, data: np.ndarray, n_clusters: int) -> Tuple[np.ndarray, KMeans]:
        """Perform K-means clustering"""
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(data)
        return clusters, kmeans
    
    def _dbscan_clustering(self, data: np.ndarray, eps: float = 0.5, 
                         min_samples: int = 5) -> Tuple[np.ndarray, DBSCAN]:
        """Perform DBSCAN clustering"""
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        clusters = dbscan.fit_predict(data)
        return clusters, dbscan
    
    def _analyze_clusters(self, data: pd.DataFrame, clusters: np.ndarray, 
                         features: List[str]) -> Dict[str, Any]:
        """Analyze cluster characteristics"""
        cluster_analysis = {}
        
        for cluster_id in np.unique(clusters):
            if cluster_id == -1:  # Noise points in DBSCAN
                continue
                
            cluster_mask = clusters == cluster_id
            cluster_data = data[cluster_mask]
            
            analysis = {
                "size": len(cluster_data),
                "percentage": len(cluster_data) / len(data) * 100,
                "feature_means": {},
                "feature_std": {}
            }
            
            for feature in features:
                if feature in cluster_data.columns and cluster_data[feature].dtype in ['int64', 'float64']:
                    analysis["feature_means"][feature] = cluster_data[feature].mean()
                    analysis["feature_std"][feature] = cluster_data[feature].std()
            
            cluster_analysis[f"cluster_{cluster_id}"] = analysis
        
        return cluster_analysis
    
    def _create_donor_segments(self, data: pd.DataFrame, clusters: np.ndarray, 
                             algorithm: str, cluster_analysis: Dict[str, Any]) -> List[DonorSegment]:
        """Create donor segment objects"""
        segments = []
        
        for cluster_id, analysis in cluster_analysis.items():
            # Generate segment name based on characteristics
            segment_name = self._generate_segment_name(analysis)
            
            # Calculate metrics
            avg_frequency = analysis["feature_means"].get("donation_frequency_per_year", 0)
            avg_volume = analysis["feature_means"].get("volume_ml", 0)
            loyalty_score = self._calculate_loyalty_score(analysis)
            risk_score = self._calculate_risk_score(analysis)
            
            # Generate recommendations
            recommendations = self._generate_cluster_recommendations(analysis)
            
            segment = DonorSegment(
                segment_name=segment_name,
                algorithm=algorithm,
                segment_size=analysis["size"],
                percentage_of_total=analysis["percentage"],
                characteristics=analysis["feature_means"],
                avg_donation_frequency=avg_frequency,
                avg_donation_volume=avg_volume,
                loyalty_score_avg=loyalty_score,
                risk_score_avg=risk_score,
                recommended_actions=recommendations
            )
            
            segments.append(segment)
        
        return segments
    
    def _generate_segment_name(self, analysis: Dict[str, Any]) -> str:
        """Generate descriptive segment name"""
        feature_means = analysis["feature_means"]
        
        # Determine segment characteristics
        if feature_means.get("donation_frequency_per_year", 0) > 3:
            frequency_desc = "High Frequency"
        elif feature_means.get("donation_frequency_per_year", 0) > 1:
            frequency_desc = "Regular"
        else:
            frequency_desc = "Occasional"
        
        if feature_means.get("age", 0) > 45:
            age_desc = "Mature"
        elif feature_means.get("age", 0) > 30:
            age_desc = "Adult"
        else:
            age_desc = "Young"
        
        if feature_means.get("volume_ml", 0) > 450:
            volume_desc = "High Volume"
        elif feature_means.get("volume_ml", 0) > 350:
            volume_desc = "Standard Volume"
        else:
            volume_desc = "Low Volume"
        
        return f"{frequency_desc} {age_desc} {volume_desc} Donors"
    
    def _calculate_loyalty_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate loyalty score for cluster"""
        frequency = analysis["feature_means"].get("donation_frequency_per_year", 0)
        volume = analysis["feature_means"].get("volume_ml", 0)
        
        # Normalize and combine factors
        loyalty_score = min(100, (frequency * 20) + (volume / 5))
        return loyalty_score
    
    def _calculate_risk_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate risk score for cluster"""
        frequency = analysis["feature_means"].get("donation_frequency_per_year", 0)
        interval = analysis["feature_means"].get("days_between_donations", 365)
        
        # Higher frequency and shorter intervals = lower risk
        if frequency > 2 and interval < 90:
            risk_score = 20  # Low risk
        elif frequency > 1 and interval < 180:
            risk_score = 50  # Medium risk
        else:
            risk_score = 80  # High risk
        
        return risk_score
    
    def _generate_cluster_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations for cluster"""
        recommendations = []
        
        frequency = analysis["feature_means"].get("donation_frequency_per_year", 0)
        volume = analysis["feature_means"].get("volume_ml", 0)
        size = analysis["size"]
        
        if frequency > 3:
            recommendations.append("Maintain regular communication schedule")
            recommendations.append("Offer priority booking and special recognition")
        elif frequency < 1:
            recommendations.append("Implement re-engagement campaign")
            recommendations.append("Send educational materials about donation importance")
        
        if volume > 450:
            recommendations.append("Monitor health parameters closely")
            recommendations.append("Provide enhanced post-donation care")
        
        if size > 1000:
            recommendations.append("Dedicated staff for this segment")
            recommendations.append("Specialized donation drives")
        
        return recommendations
    
    def _get_model_info(self, model, algorithm: str) -> Dict[str, Any]:
        """Get model information"""
        info = {"algorithm": algorithm}
        
        if algorithm == "kmeans":
            info["inertia"] = model.inertia_
            info["n_clusters"] = model.n_clusters
            info["cluster_centers"] = model.cluster_centers_.tolist()
        elif algorithm == "dbscan":
            info["eps"] = model.eps
            info["min_samples"] = model.min_samples
            info["n_noise_points"] = list(model.labels_).count(-1)
        
        return info
    
    def perform_classification_analysis(self, data: pd.DataFrame, 
                                      target_variable: str,
                                      algorithm: str = "decision_tree",
                                      features: List[str] = None) -> Dict[str, Any]:
        """Perform classification analysis for donor behavior prediction"""
        if features is None:
            features = self._get_default_classification_features(data)
        
        # Prepare data
        X, y = self._prepare_classification_data(data, target_variable, features)
        
        if len(X) == 0:
            return {"error": "No valid data for classification"}
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        if algorithm == "decision_tree":
            model = self._train_decision_tree(X_train, y_train)
        elif algorithm == "svm":
            model = self._train_svm(X_train, y_train)
        elif algorithm == "random_forest":
            model = self._train_random_forest(X_train, y_train)
        else:
            raise ValueError(f"Unsupported classification algorithm: {algorithm}")
        
        # Evaluate model
        predictions = model.predict(X_test)
        performance = self._evaluate_classification(y_test, predictions)
        
        # Feature importance
        feature_importance = self._get_feature_importance(model, features, algorithm)
        
        return {
            "algorithm": algorithm,
            "target_variable": target_variable,
            "features": features,
            "performance": performance,
            "feature_importance": feature_importance,
            "model_info": self._get_classification_model_info(model, algorithm)
        }
    
    def _get_default_classification_features(self, data: pd.DataFrame) -> List[str]:
        """Get default features for classification"""
        available_features = []
        
        potential_features = [
            "age", "gender", "blood_type", "volume_ml", "donation_frequency_per_year",
            "days_between_donations", "eligibility_score", "season", "day_of_week"
        ]
        
        for feature in potential_features:
            if feature in data.columns:
                available_features.append(feature)
        
        return available_features
    
    def _prepare_classification_data(self, data: pd.DataFrame, target_variable: str, 
                                   features: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for classification"""
        # Extract features
        X_data = data[features].copy()
        y_data = data[target_variable].copy()
        
        # Remove rows with missing target
        valid_mask = ~y_data.isna()
        X_data = X_data[valid_mask]
        y_data = y_data[valid_mask]
        
        # Handle categorical features
        for feature in features:
            if X_data[feature].dtype == 'object':
                if feature not in self.label_encoders:
                    self.label_encoders[feature] = LabelEncoder()
                X_data[feature] = self.label_encoders[feature].fit_transform(X_data[feature].astype(str))
        
        # Handle missing values in features
        X_data = X_data.fillna(X_data.mean())
        
        # Encode target if categorical
        if y_data.dtype == 'object':
            if target_variable not in self.label_encoders:
                self.label_encoders[target_variable] = LabelEncoder()
            y_data = self.label_encoders[target_variable].fit_transform(y_data.astype(str))
        
        return X_data.values, y_data.values
    
    def _train_decision_tree(self, X_train: np.ndarray, y_train: np.ndarray) -> DecisionTreeClassifier:
        """Train decision tree classifier"""
        model = DecisionTreeClassifier(random_state=42, max_depth=10)
        model.fit(X_train, y_train)
        return model
    
    def _train_svm(self, X_train: np.ndarray, y_train: np.ndarray) -> SVC:
        """Train SVM classifier"""
        model = SVC(random_state=42, probability=True)
        model.fit(X_train, y_train)
        return model
    
    def _train_random_forest(self, X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
        """Train random forest classifier"""
        model = RandomForestClassifier(random_state=42, n_estimators=100)
        model.fit(X_train, y_train)
        return model
    
    def _evaluate_classification(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        """Evaluate classification performance"""
        accuracy = accuracy_score(y_true, y_pred)
        
        # Cross-validation scores
        cv_scores = cross_val_score(RandomForestClassifier(random_state=42), 
                                  np.column_stack([np.arange(len(y_true)), y_true]), 
                                  y_true, cv=5)
        
        return {
            "accuracy": accuracy,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
            "classification_report": classification_report(y_true, y_pred, output_dict=True)
        }
    
    def _get_feature_importance(self, model, features: List[str], algorithm: str) -> Dict[str, float]:
        """Get feature importance from model"""
        if hasattr(model, 'feature_importances_'):
            importance_dict = dict(zip(features, model.feature_importances_))
            return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
        else:
            return {}
    
    def _get_classification_model_info(self, model, algorithm: str) -> Dict[str, Any]:
        """Get classification model information"""
        info = {"algorithm": algorithm}
        
        if algorithm == "decision_tree":
            info["max_depth"] = model.max_depth
            info["n_features"] = model.n_features_in_
        elif algorithm == "random_forest":
            info["n_estimators"] = model.n_estimators
            info["max_depth"] = model.max_depth
            info["n_features"] = model.n_features_in_
        
        return info
    
    def perform_association_rule_mining(self, data: pd.DataFrame, 
                                      min_support: float = 0.1,
                                      min_confidence: float = 0.7) -> Dict[str, Any]:
        """Perform association rule mining for donor behavior patterns"""
        # Prepare transaction data
        transaction_data = self._prepare_transaction_data(data)
        
        if transaction_data.empty:
            return {"error": "Insufficient data for association rule mining"}
        
        # Apply Apriori algorithm
        frequent_itemsets = apriori(transaction_data, min_support=min_support, use_colnames=True)
        
        if frequent_itemsets.empty:
            return {"error": "No frequent itemsets found with given support threshold"}
        
        # Generate association rules
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
        
        if rules.empty:
            return {"error": "No association rules found with given confidence threshold"}
        
        # Analyze rules
        rule_analysis = self._analyze_association_rules(rules, data)
        
        return {
            "min_support": min_support,
            "min_confidence": min_confidence,
            "frequent_itemsets_count": len(frequent_itemsets),
            "association_rules_count": len(rules),
            "rules": self._format_association_rules(rules),
            "rule_analysis": rule_analysis
        }
    
    def _prepare_transaction_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare transaction data for association rule mining"""
        # Create binary features for common donor characteristics
        transactions = []
        
        for _, row in data.iterrows():
            transaction_items = []
            
            # Blood type
            if "blood_type" in row and pd.notna(row["blood_type"]):
                transaction_items.append(f"blood_type_{row['blood_type']}")
            
            # Age group
            if "age" in row and pd.notna(row["age"]):
                age = row["age"]
                if age < 25:
                    transaction_items.append("age_group_18-25")
                elif age < 35:
                    transaction_items.append("age_group_26-35")
                elif age < 45:
                    transaction_items.append("age_group_36-45")
                elif age < 55:
                    transaction_items.append("age_group_46-55")
                else:
                    transaction_items.append("age_group_56+")
            
            # Gender
            if "gender" in row and pd.notna(row["gender"]):
                transaction_items.append(f"gender_{row['gender']}")
            
            # Donation type
            if "donation_type" in row and pd.notna(row["donation_type"]):
                transaction_items.append(f"donation_type_{row['donation_type']}")
            
            # Volume category
            if "volume_ml" in row and pd.notna(row["volume_ml"]):
                volume = row["volume_ml"]
                if volume < 350:
                    transaction_items.append("volume_low")
                elif volume < 450:
                    transaction_items.append("volume_standard")
                else:
                    transaction_items.append("volume_high")
            
            # Season
            if "donation_date" in row and pd.notna(row["donation_date"]):
                date = pd.to_datetime(row["donation_date"])
                month = date.month
                if month in [12, 1, 2]:
                    transaction_items.append("season_winter")
                elif month in [3, 4, 5]:
                    transaction_items.append("season_spring")
                elif month in [6, 7, 8]:
                    transaction_items.append("season_summer")
                else:
                    transaction_items.append("season_fall")
            
            transactions.append(transaction_items)
        
        # Convert to one-hot encoded DataFrame
        all_items = list(set(item for transaction in transactions for item in transaction))
        
        transaction_matrix = []
        for transaction in transactions:
            row = [1 if item in transaction else 0 for item in all_items]
            transaction_matrix.append(row)
        
        return pd.DataFrame(transaction_matrix, columns=all_items)
    
    def _analyze_association_rules(self, rules: pd.DataFrame, original_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze association rules for insights"""
        analysis = {
            "strongest_rules": [],
            "most_surprising_rules": [],
            "actionable_insights": []
        }
        
        # Sort rules by lift (most interesting)
        rules_sorted = rules.sort_values('lift', ascending=False)
        
        # Get top 10 strongest rules
        for _, rule in rules_sorted.head(10).iterrows():
            analysis["strongest_rules"].append({
                "antecedents": list(rule['antecedents']),
                "consequents": list(rule['consequents']),
                "support": rule['support'],
                "confidence": rule['confidence'],
                "lift": rule['lift']
            })
        
        # Generate actionable insights
        for _, rule in rules_sorted.head(5).iterrows():
            antecedents = list(rule['antecedents'])
            consequents = list(rule['consequents'])
            
            if rule['lift'] > 1.5 and rule['confidence'] > 0.8:
                insight = f"Strong association: {antecedents} → {consequents}"
                analysis["actionable_insights"].append(insight)
        
        return analysis
    
    def _format_association_rules(self, rules: pd.DataFrame) -> List[Dict[str, Any]]:
        """Format association rules for output"""
        formatted_rules = []
        
        for _, rule in rules.iterrows():
            formatted_rule = {
                "antecedents": list(rule['antecedents']),
                "consequents": list(rule['consequents']),
                "support": float(rule['support']),
                "confidence": float(rule['confidence']),
                "lift": float(rule['lift']),
                "leverage": float(rule['leverage']),
                "conviction": float(rule['conviction'])
            }
            formatted_rules.append(formatted_rule)
        
        return formatted_rules
    
    def identify_behavioral_patterns(self, data: pd.DataFrame) -> Dict[str, DonorBehaviorPattern]:
        """Identify donor behavioral patterns from historical data"""
        patterns = {}
        
        # Frequent donor pattern
        frequent_pattern = self._identify_frequent_donors(data)
        patterns["frequent_donor"] = frequent_pattern
        
        # Seasonal donor pattern
        seasonal_pattern = self._identify_seasonal_donors(data)
        patterns["seasonal_donor"] = seasonal_pattern
        
        # Irregular donor pattern
        irregular_pattern = self._identify_irregular_donors(data)
        patterns["irregular_donor"] = irregular_pattern
        
        # New donor pattern
        new_pattern = self._identify_new_donors(data)
        patterns["new_donor"] = new_pattern
        
        return patterns
    
    def _identify_frequent_donors(self, data: pd.DataFrame) -> DonorBehaviorPattern:
        """Identify frequent donor behavior pattern"""
        if "donor_id" not in data.columns:
            return DonorBehaviorPattern(pattern_type="frequent_donor", donor_count=0)
        
        # Calculate donation frequency per donor
        donor_stats = data.groupby("donor_id").agg({
            "donation_date": ["count", "min", "max"],
            "volume_ml": "sum"
        }).reset_index()
        
        donor_stats.columns = ["donor_id", "donation_count", "first_donation", "last_donation", "total_volume"]
        
        # Define frequent donors (more than 3 donations per year)
        donor_stats["days_active"] = (donor_stats["last_donation"] - donor_stats["first_donation"]).dt.days
        donor_stats["years_active"] = donor_stats["days_active"] / 365.25
        donor_stats["frequency_per_year"] = donor_stats["donation_count"] / donor_stats["years_active"]
        
        frequent_donors = donor_stats[donor_stats["frequency_per_year"] >= 3]
        
        return DonorBehaviorPattern(
            pattern_type="frequent_donor",
            donor_count=len(frequent_donors),
            pattern_description="Donors who donate 3+ times per year consistently",
            key_indicators=["High donation frequency", "Regular donation intervals", "High total volume"],
            avg_donation_interval=frequent_donors["days_active"].mean() / frequent_donors["donation_count"].mean() if len(frequent_donors) > 0 else None,
            retention_probability=0.85 if len(frequent_donors) > 0 else 0
        )
    
    def _identify_seasonal_donors(self, data: pd.DataFrame) -> DonorBehaviorPattern:
        """Identify seasonal donor behavior pattern"""
        if "donor_id" not in data.columns or "donation_date" not in data.columns:
            return DonorBehaviorPattern(pattern_type="seasonal_donor", donor_count=0)
        
        # Analyze donation patterns by month
        data["month"] = pd.to_datetime(data["donation_date"]).dt.month
        
        # Find donors with strong seasonal preferences
        seasonal_donors = []
        
        for donor_id in data["donor_id"].unique():
            donor_data = data[data["donor_id"] == donor_id]
            month_counts = donor_data["month"].value_counts()
            
            if len(month_counts) >= 3:  # At least 3 donations
                # Check if 50%+ donations are in 3 consecutive months
                month_counts_sorted = month_counts.sort_index()
                for i in range(1, 11):  # Months 1-11 (0-indexed)
                    window_sum = month_counts_sorted.get(i, 0) + month_counts_sorted.get(i+1, 0) + month_counts_sorted.get(i+2, 0)
                    if window_sum >= len(donor_data) * 0.5:
                        seasonal_donors.append(donor_id)
                        break
        
        seasonal_trends = {
            "winter": len([d for d in seasonal_donors if self._get_primary_season(data, d) == "winter"]),
            "spring": len([d for d in seasonal_donors if self._get_primary_season(data, d) == "spring"]),
            "summer": len([d for d in seasonal_donors if self._get_primary_season(data, d) == "summer"]),
            "fall": len([d for d in seasonal_donors if self._get_primary_season(data, d) == "fall"])
        }
        
        return DonorBehaviorPattern(
            pattern_type="seasonal_donor",
            donor_count=len(seasonal_donors),
            pattern_description="Donors who show strong seasonal donation preferences",
            key_indicators=["Seasonal concentration", "Predictable timing", "Weather-dependent behavior"],
            seasonal_trends=seasonal_trends,
            retention_probability=0.75
        )
    
    def _identify_irregular_donors(self, data: pd.DataFrame) -> DonorBehaviorPattern:
        """Identify irregular donor behavior pattern"""
        if "donor_id" not in data.columns:
            return DonorBehaviorPattern(pattern_type="irregular_donor", donor_count=0)
        
        # Calculate donation intervals
        donor_intervals = {}
        
        for donor_id in data["donor_id"].unique():
            donor_data = data[data["donor_id"] == donor_id].sort_values("donation_date")
            if len(donor_data) >= 2:
                intervals = donor_data["donation_date"].diff().dt.days.dropna()
                donor_intervals[donor_id] = {
                    "mean_interval": intervals.mean(),
                    "std_interval": intervals.std(),
                    "donation_count": len(donor_data)
                }
        
        # Define irregular donors (high variability in donation intervals)
        irregular_donors = []
        for donor_id, stats in donor_intervals.items():
            if stats["std_interval"] > stats["mean_interval"] * 0.5:  # High variability
                irregular_donors.append(donor_id)
        
        return DonorBehaviorPattern(
            pattern_type="irregular_donor",
            donor_count=len(irregular_donors),
            pattern_description="Donors with unpredictable donation patterns",
            key_indicators=["Variable donation intervals", "Inconsistent timing", "Opportunistic behavior"],
            avg_donation_interval=np.mean([stats["mean_interval"] for stats in donor_intervals.values()]) if donor_intervals else None,
            retention_probability=0.45,
            risk_factors=["High churn risk", "Difficult to predict", "Requires targeted engagement"]
        )
    
    def _identify_new_donors(self, data: pd.DataFrame) -> DonorBehaviorPattern:
        """Identify new donor behavior pattern"""
        if "donor_id" not in data.columns or "donation_date" not in data.columns:
            return DonorBehaviorPattern(pattern_type="new_donor", donor_count=0)
        
        # Find donors who donated in the last 90 days
        cutoff_date = datetime.now() - timedelta(days=90)
        recent_donations = data[pd.to_datetime(data["donation_date"]) >= cutoff_date]
        
        # Find first-time donors
        all_donors = set(data["donor_id"].unique())
        repeat_donors = set(data[data["donor_id"].duplicated(keep=False)]["donor_id"].unique())
        new_donors = list(all_donors - repeat_donors)
        
        recent_new_donors = recent_donations[recent_donations["donor_id"].isin(new_donors)]
        
        return DonorBehaviorPattern(
            pattern_type="new_donor",
            donor_count=len(recent_new_donors["donor_id"].unique()),
            pattern_description="First-time donors in the last 90 days",
            key_indicators=["First donation", "Recent activity", "High potential"],
            retention_probability=0.65,
            risk_factors=["High initial dropout risk", "Need education and support"]
        )
    
    def _get_primary_season(self, data: pd.DataFrame, donor_id: str) -> str:
        """Get primary donation season for a donor"""
        donor_data = data[data["donor_id"] == donor_id]
        donor_data["month"] = pd.to_datetime(donor_data["donation_date"]).dt.month
        
        month_counts = donor_data["month"].value_counts()
        
        # Map months to seasons
        season_counts = {"winter": 0, "spring": 0, "summer": 0, "fall": 0}
        
        for month, count in month_counts.items():
            if month in [12, 1, 2]:
                season_counts["winter"] += count
            elif month in [3, 4, 5]:
                season_counts["spring"] += count
            elif month in [6, 7, 8]:
                season_counts["summer"] += count
            else:
                season_counts["fall"] += count
        
        return max(season_counts, key=season_counts.get)
    
    def generate_intelligent_recommendations(self, data: pd.DataFrame, 
                                           analysis_results: Dict[str, Any]) -> List[RecommendationEngine]:
        """Generate intelligent recommendations based on analysis results"""
        recommendations = []
        
        # Donor recall recommendations
        recall_recommendations = self._generate_recall_recommendations(data, analysis_results)
        recommendations.extend(recall_recommendations)
        
        # Inventory optimization recommendations
        inventory_recommendations = self._generate_inventory_recommendations(data, analysis_results)
        recommendations.extend(inventory_recommendations)
        
        # Campaign targeting recommendations
        campaign_recommendations = self._generate_campaign_recommendations(data, analysis_results)
        recommendations.extend(campaign_recommendations)
        
        return recommendations
    
    def _generate_recall_recommendations(self, data: pd.DataFrame, 
                                       analysis_results: Dict[str, Any]) -> List[RecommendationEngine]:
        """Generate donor recall recommendations"""
        recommendations = []
        
        # Target irregular donors for re-engagement
        if "behavioral_patterns" in analysis_results:
            irregular_pattern = analysis_results["behavioral_patterns"].get("irregular_donor")
            if irregular_pattern and irregular_pattern.donor_count > 0:
                recommendation = RecommendationEngine(
                    recommendation_type="donor_recall",
                    target_audience="irregular_donors",
                    priority_score=75,
                    expected_impact={"retention_improvement": 25, "donation_increase": 15},
                    action_items=[
                        "Send personalized re-engagement emails",
                        "Offer flexible scheduling options",
                        "Provide donation impact reports"
                    ],
                    success_probability=0.65,
                    cost_estimate=5000
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_inventory_recommendations(self, data: pd.DataFrame, 
                                          analysis_results: Dict[str, Any]) -> List[RecommendationEngine]:
        """Generate inventory optimization recommendations"""
        recommendations = []
        
        # Blood type inventory balancing
        if "trend_analysis" in analysis_results:
            blood_type_trends = analysis_results["trend_analysis"].get("blood_type")
            if blood_type_trends:
                recommendation = RecommendationEngine(
                    recommendation_type="inventory_optimization",
                    target_audience="blood_type_management",
                    priority_score=80,
                    expected_impact={"waste_reduction": 30, "availability_improvement": 20},
                    action_items=[
                        "Adjust collection targets based on demand forecasts",
                        "Implement dynamic pricing for rare blood types",
                        "Cross-regional blood sharing program"
                    ],
                    success_probability=0.75,
                    cost_estimate=15000
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_campaign_recommendations(self, data: pd.DataFrame, 
                                         analysis_results: Dict[str, Any]) -> List[RecommendationEngine]:
        """Generate campaign targeting recommendations"""
        recommendations = []
        
        # Target specific donor segments
        if "clustering_analysis" in analysis_results:
            segments = analysis_results["clustering_analysis"].get("segments", [])
            for segment in segments:
                if segment.segment_size > 100 and segment.loyalty_score_avg < 50:
                    recommendation = RecommendationEngine(
                        recommendation_type="campaign_targeting",
                        target_audience=segment.segment_name,
                        priority_score=70,
                        expected_impact={"campaign_response": 35, "new_donors": 20},
                        action_items=[
                            f"Create targeted messaging for {segment.segment_name}",
                            f"Design campaign around {segment.characteristics}",
                            "Use multi-channel communication strategy"
                        ],
                        success_probability=0.70,
                        cost_estimate=8000
                    )
                    recommendations.append(recommendation)
        
        return recommendations
