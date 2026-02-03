"""
Association rule mining and analysis for blood domain
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

from ..models.analytics import DonorSegment, RecommendationEngine
from ..config import Config

class AssociationAnalyzer:
    """Advanced association rule mining for blood domain insights"""
    
    def __init__(self):
        self.transaction_encoder = TransactionEncoder()
        self.label_encoders = {}
        self.association_cache = {}
    
    def discover_association_rules(self, data: pd.DataFrame, 
                                 min_support: float = 0.1,
                                 min_confidence: float = 0.7,
                                 min_lift: float = 1.0,
                                 algorithm: str = "apriori") -> Dict[str, Any]:
        """Discover association rules in donor data"""
        
        # Prepare transaction data
        transaction_data = self._prepare_transaction_data(data)
        
        if transaction_data.empty:
            return {"error": "Insufficient data for association rule mining"}
        
        # Generate frequent itemsets
        frequent_itemsets = self._generate_frequent_itemsets(
            transaction_data, min_support, algorithm
        )
        
        if frequent_itemsets.empty:
            return {"error": f"No frequent itemsets found with min_support={min_support}"}
        
        # Generate association rules
        rules = self._generate_association_rules(
            frequent_itemsets, min_confidence, min_lift
        )
        
        if rules.empty:
            return {"error": f"No association rules found with min_confidence={min_confidence}"}
        
        # Analyze rules
        rule_analysis = self._analyze_association_rules(rules, data)
        
        # Generate insights
        insights = self._generate_association_insights(rules, rule_analysis)
        
        # Create recommendations
        recommendations = self._create_association_recommendations(rules, rule_analysis)
        
        return {
            "algorithm": algorithm,
            "parameters": {
                "min_support": min_support,
                "min_confidence": min_confidence,
                "min_lift": min_lift
            },
            "frequent_itemsets": self._format_frequent_itemsets(frequent_itemsets),
            "association_rules": self._format_association_rules(rules),
            "rule_analysis": rule_analysis,
            "insights": insights,
            "recommendations": recommendations,
            "summary": self._generate_rule_summary(rules)
        }
    
    def _prepare_transaction_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare transaction data for association rule mining"""
        transactions = []
        
        for _, row in data.iterrows():
            transaction_items = []
            
            # Demographic attributes
            if "age" in row and pd.notna(row["age"]):
                age = row["age"]
                if age < 25:
                    transaction_items.append("age_18-25")
                elif age < 35:
                    transaction_items.append("age_26-35")
                elif age < 45:
                    transaction_items.append("age_36-45")
                elif age < 55:
                    transaction_items.append("age_46-55")
                else:
                    transaction_items.append("age_56+")
            
            if "gender" in row and pd.notna(row["gender"]):
                transaction_items.append(f"gender_{row['gender'].lower()}")
            
            if "blood_type" in row and pd.notna(row["blood_type"]):
                transaction_items.append(f"blood_type_{row['blood_type'].replace('+', 'plus').replace('-', 'minus')}")
            
            # Donation attributes
            if "donation_type" in row and pd.notna(row["donation_type"]):
                transaction_items.append(f"donation_type_{row['donation_type'].lower()}")
            
            if "volume_ml" in row and pd.notna(row["volume_ml"]):
                volume = row["volume_ml"]
                if volume < 350:
                    transaction_items.append("volume_low")
                elif volume < 450:
                    transaction_items.append("volume_standard")
                else:
                    transaction_items.append("volume_high")
            
            # Temporal attributes
            if "donation_date" in row and pd.notna(row["donation_date"]):
                date = pd.to_datetime(row["donation_date"])
                month = date.month
                day_of_week = date.dayofweek
                
                # Season
                if month in [12, 1, 2]:
                    transaction_items.append("season_winter")
                elif month in [3, 4, 5]:
                    transaction_items.append("season_spring")
                elif month in [6, 7, 8]:
                    transaction_items.append("season_summer")
                else:
                    transaction_items.append("season_fall")
                
                # Day type
                if day_of_week >= 5:
                    transaction_items.append("day_weekend")
                else:
                    transaction_items.append("day_weekday")
                
                # Time of day (if available)
                if "donation_time" in row and pd.notna(row["donation_time"]):
                    time = pd.to_datetime(row["donation_time"]).hour
                    if time < 12:
                        transaction_items.append("time_morning")
                    elif time < 17:
                        transaction_items.append("time_afternoon")
                    else:
                        transaction_items.append("time_evening")
            
            # Location attributes
            if "location" in row and pd.notna(row["location"]):
                location = str(row["location"]).lower()
                if "hospital" in location:
                    transaction_items.append("location_hospital")
                elif "center" in location:
                    transaction_items.append("location_center")
                elif "clinic" in location:
                    transaction_items.append("location_clinic")
                else:
                    transaction_items.append("location_other")
            
            # Donor category
            if "category" in row and pd.notna(row["category"]):
                transaction_items.append(f"category_{row['category'].lower()}")
            
            # Health indicators
            if "hemoglobin_level" in row and pd.notna(row["hemoglobin_level"]):
                hgb = row["hemoglobin_level"]
                if hgb < 12.5:
                    transaction_items.append("hemoglobin_low")
                elif hgb > 16.0:
                    transaction_items.append("hemoglobin_high")
                else:
                    transaction_items.append("hemoglobin_normal")
            
            if "blood_pressure_systolic" in row and pd.notna(row["blood_pressure_systolic"]):
                systolic = row["blood_pressure_systolic"]
                if systolic > 140:
                    transaction_items.append("bp_high")
                elif systolic < 120:
                    transaction_items.append("bp_low")
                else:
                    transaction_items.append("bp_normal")
            
            # Frequency indicators (if available)
            if "donation_frequency_per_year" in row and pd.notna(row["donation_frequency_per_year"]):
                freq = row["donation_frequency_per_year"]
                if freq >= 3:
                    transaction_items.append("frequency_high")
                elif freq >= 1:
                    transaction_items.append("frequency_medium")
                else:
                    transaction_items.append("frequency_low")
            
            # Loyalty indicators
            if "loyalty_score" in row and pd.notna(row["loyalty_score"]):
                loyalty = row["loyalty_score"]
                if loyalty >= 80:
                    transaction_items.append("loyalty_high")
                elif loyalty >= 50:
                    transaction_items.append("loyalty_medium")
                else:
                    transaction_items.append("loyalty_low")
            
            transactions.append(transaction_items)
        
        # Convert to one-hot encoded DataFrame
        if not transactions:
            return pd.DataFrame()
        
        try:
            encoded_array = self.transaction_encoder.fit_transform(transactions)
            feature_names = self.transaction_encoder.columns_
            return pd.DataFrame(encoded_array, columns=feature_names)
        except:
            return pd.DataFrame()
    
    def _generate_frequent_itemsets(self, transaction_data: pd.DataFrame, 
                                  min_support: float, algorithm: str) -> pd.DataFrame:
        """Generate frequent itemsets using specified algorithm"""
        try:
            if algorithm == "apriori":
                frequent_itemsets = apriori(transaction_data, min_support=min_support, 
                                          use_colnames=True, max_len=4)
            elif algorithm == "fpgrowth":
                frequent_itemsets = fpgrowth(transaction_data, min_support=min_support, 
                                           use_colnames=True, max_len=4)
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
            
            return frequent_itemsets
        except Exception as e:
            print(f"Error generating frequent itemsets: {str(e)}")
            return pd.DataFrame()
    
    def _generate_association_rules(self, frequent_itemsets: pd.DataFrame, 
                                  min_confidence: float, min_lift: float) -> pd.DataFrame:
        """Generate association rules from frequent itemsets"""
        try:
            rules = association_rules(frequent_itemsets, metric="confidence", 
                                   min_threshold=min_confidence)
            
            # Filter by lift
            if min_lift > 0:
                rules = rules[rules['lift'] >= min_lift]
            
            return rules
        except Exception as e:
            print(f"Error generating association rules: {str(e)}")
            return pd.DataFrame()
    
    def _analyze_association_rules(self, rules: pd.DataFrame, original_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze discovered association rules"""
        analysis = {
            "rule_statistics": self._calculate_rule_statistics(rules),
            "rule_categories": self._categorize_rules(rules),
            "interesting_rules": self._identify_interesting_rules(rules),
            "actionable_rules": self._identify_actionable_rules(rules),
            "surprising_rules": self._identify_surprising_rules(rules)
        }
        
        return analysis
    
    def _calculate_rule_statistics(self, rules: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive statistics for association rules"""
        if rules.empty:
            return {}
        
        stats = {
            "total_rules": len(rules),
            "avg_support": rules['support'].mean(),
            "avg_confidence": rules['confidence'].mean(),
            "avg_lift": rules['lift'].mean(),
            "max_support": rules['support'].max(),
            "max_confidence": rules['confidence'].max(),
            "max_lift": rules['lift'].max(),
            "min_support": rules['support'].min(),
            "min_confidence": rules['confidence'].min(),
            "min_lift": rules['lift'].min()
        }
        
        # Rule length distribution
        antecedent_lengths = rules['antecedents'].apply(len)
        consequent_lengths = rules['consequents'].apply(len)
        
        stats["antecedent_length_distribution"] = {
            "mean": antecedent_lengths.mean(),
            "max": antecedent_lengths.max(),
            "min": antecedent_lengths.min()
        }
        
        stats["consequent_length_distribution"] = {
            "mean": consequent_lengths.mean(),
            "max": consequent_lengths.max(),
            "min": consequent_lengths.min()
        }
        
        return stats
    
    def _categorize_rules(self, rules: pd.DataFrame) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize association rules by type"""
        categories = {
            "demographic_rules": [],
            "behavioral_rules": [],
            "temporal_rules": [],
            "health_rules": [],
            "location_rules": [],
            "cross_domain_rules": []
        }
        
        for _, rule in rules.iterrows():
            antecedents = list(rule['antecedents'])
            consequents = list(rule['consequents'])
            all_items = antecedents + consequents
            
            rule_info = {
                "antecedents": antecedents,
                "consequents": consequents,
                "support": rule['support'],
                "confidence": rule['confidence'],
                "lift": rule['lift']
            }
            
            # Categorize based on item types
            if any(item.startswith(("age_", "gender_", "blood_type_")) for item in all_items):
                categories["demographic_rules"].append(rule_info)
            
            if any(item.startswith(("donation_type_", "volume_", "frequency_", "loyalty_")) for item in all_items):
                categories["behavioral_rules"].append(rule_info)
            
            if any(item.startswith(("season_", "day_", "time_")) for item in all_items):
                categories["temporal_rules"].append(rule_info)
            
            if any(item.startswith(("hemoglobin_", "bp_")) for item in all_items):
                categories["health_rules"].append(rule_info)
            
            if any(item.startswith("location_") for item in all_items):
                categories["location_rules"].append(rule_info)
            
            # Cross-domain rules (items from different categories)
            domains = set()
            for item in all_items:
                if item.startswith(("age_", "gender_", "blood_type_")):
                    domains.add("demographic")
                elif item.startswith(("donation_type_", "volume_", "frequency_", "loyalty_")):
                    domains.add("behavioral")
                elif item.startswith(("season_", "day_", "time_")):
                    domains.add("temporal")
                elif item.startswith(("hemoglobin_", "bp_")):
                    domains.add("health")
                elif item.startswith("location_"):
                    domains.add("location")
            
            if len(domains) > 1:
                categories["cross_domain_rules"].append(rule_info)
        
        return categories
    
    def _identify_interesting_rules(self, rules: pd.DataFrame, top_n: int = 10) -> List[Dict[str, Any]]:
        """Identify most interesting rules based on multiple criteria"""
        if rules.empty:
            return []
        
        # Calculate interestingness score
        rules['interestingness'] = (
            rules['lift'] * 0.4 + 
            rules['confidence'] * 0.3 + 
            rules['support'] * 0.3
        )
        
        # Sort by interestingness
        interesting_rules = rules.nlargest(top_n, 'interestingness')
        
        formatted_rules = []
        for _, rule in interesting_rules.iterrows():
            formatted_rules.append({
                "antecedents": list(rule['antecedents']),
                "consequents": list(rule['consequents']),
                "support": rule['support'],
                "confidence": rule['confidence'],
                "lift": rule['lift'],
                "interestingness": rule['interestingness']
            })
        
        return formatted_rules
    
    def _identify_actionable_rules(self, rules: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identify actionable rules for business decisions"""
        actionable_rules = []
        
        for _, rule in rules.iterrows():
            antecedents = list(rule['antecedents'])
            consequents = list(rule['consequents'])
            
            # Define actionability criteria
            is_actionable = False
            action_type = None
            
            # High confidence rules with demographic antecedents
            if (rule['confidence'] >= 0.8 and 
                any(item.startswith(("age_", "gender_", "blood_type_")) for item in antecedents)):
                is_actionable = True
                action_type = "targeted_marketing"
            
            # High lift rules with temporal antecedents
            if (rule['lift'] >= 2.0 and 
                any(item.startswith(("season_", "day_")) for item in antecedents)):
                is_actionable = True
                action_type = "seasonal_campaign"
            
            # Rules involving loyalty or frequency
            if (any(item.startswith(("loyalty_", "frequency_")) for item in consequents) and 
                rule['confidence'] >= 0.7):
                is_actionable = True
                action_type = "retention_strategy"
            
            # Health-related rules
            if (any(item.startswith(("hemoglobin_", "bp_")) for item in antecedents) and 
                rule['confidence'] >= 0.6):
                is_actionable = True
                action_type = "health_screening"
            
            if is_actionable:
                actionable_rules.append({
                    "antecedents": antecedents,
                    "consequents": consequents,
                    "support": rule['support'],
                    "confidence": rule['confidence'],
                    "lift": rule['lift'],
                    "action_type": action_type
                })
        
        return actionable_rules
    
    def _identify_surprising_rules(self, rules: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identify surprising or counter-intuitive rules"""
        surprising_rules = []
        
        for _, rule in rules.iterrows():
            antecedents = list(rule['antecedents'])
            consequents = list(rule['consequents'])
            
            # Define surprising criteria
            is_surprising = False
            surprise_reason = None
            
            # Very high lift rules (unexpected associations)
            if rule['lift'] >= 3.0:
                is_surprising = True
                surprise_reason = "very_high_lift"
            
            # Counter-intuitive associations
            if (any("low" in item for item in antecedents) and 
                any("high" in item for item in consequents)):
                is_surprising = True
                surprise_reason = "counter_intuitive"
            
            # Cross-domain high confidence rules
            domains = set()
            for item in antecedents + consequents:
                if item.startswith(("age_", "gender_", "blood_type_")):
                    domains.add("demographic")
                elif item.startswith(("donation_type_", "volume_")):
                    domains.add("behavioral")
                elif item.startswith(("season_", "day_")):
                    domains.add("temporal")
            
            if (len(domains) >= 3 and rule['confidence'] >= 0.8):
                is_surprising = True
                surprise_reason = "cross_domain_high_confidence"
            
            if is_surprising:
                surprising_rules.append({
                    "antecedents": antecedents,
                    "consequents": consequents,
                    "support": rule['support'],
                    "confidence": rule['confidence'],
                    "lift": rule['lift'],
                    "surprise_reason": surprise_reason
                })
        
        return surprising_rules
    
    def _format_frequent_itemsets(self, frequent_itemsets: pd.DataFrame) -> List[Dict[str, Any]]:
        """Format frequent itemsets for output"""
        formatted = []
        
        for _, itemset in frequent_itemsets.iterrows():
            formatted.append({
                "items": list(itemset['itemsets']),
                "support": itemset['support'],
                "item_count": len(itemset['itemsets'])
            })
        
        return formatted
    
    def _format_association_rules(self, rules: pd.DataFrame) -> List[Dict[str, Any]]:
        """Format association rules for output"""
        formatted = []
        
        for _, rule in rules.iterrows():
            formatted.append({
                "antecedents": list(rule['antecedents']),
                "consequents": list(rule['consequents']),
                "support": rule['support'],
                "confidence": rule['confidence'],
                "lift": rule['lift'],
                "leverage": rule['leverage'],
                "conviction": rule['conviction']
            })
        
        return formatted
    
    def _generate_association_insights(self, rules: pd.DataFrame, 
                                     rule_analysis: Dict[str, Any]) -> List[str]:
        """Generate insights from association rules"""
        insights = []
        
        if rules.empty:
            return ["No association rules discovered"]
        
        # General insights
        stats = rule_analysis.get("rule_statistics", {})
        if stats:
            avg_lift = stats.get("avg_lift", 0)
            if avg_lift > 1.5:
                insights.append("Strong associations found between donor attributes")
            elif avg_lift > 1.2:
                insights.append("Moderate associations detected in donor data")
            else:
                insights.append("Weak associations - donor behaviors largely independent")
        
        # Category-specific insights
        categories = rule_analysis.get("rule_categories", {})
        
        if categories.get("demographic_rules"):
            insights.append(f"Found {len(categories['demographic_rules'])} demographic association patterns")
        
        if categories.get("temporal_rules"):
            insights.append(f"Discovered {len(categories['temporal_rules'])} temporal donation patterns")
        
        if categories.get("cross_domain_rules"):
            insights.append(f"Identified {len(categories['cross_domain_rules'])} cross-domain relationships")
        
        # Actionable insights
        actionable = rule_analysis.get("actionable_rules", [])
        if actionable:
            insights.append(f"Found {len(actionable)} actionable rules for business decisions")
        
        # Surprising insights
        surprising = rule_analysis.get("surprising_rules", [])
        if surprising:
            insights.append(f"Discovered {len(surprising)} surprising patterns requiring investigation")
        
        return insights
    
    def _create_association_recommendations(self, rules: pd.DataFrame, 
                                          rule_analysis: Dict[str, Any]) -> List[RecommendationEngine]:
        """Create recommendations based on association rules"""
        recommendations = []
        
        actionable_rules = rule_analysis.get("actionable_rules", [])
        
        for rule in actionable_rules[:5]:  # Top 5 actionable rules
            action_type = rule["action_type"]
            antecedents = rule["antecedents"]
            consequents = rule["consequents"]
            
            if action_type == "targeted_marketing":
                recommendation = RecommendationEngine(
                    recommendation_type="targeted_marketing",
                    target_audience=f"donors with {', '.join(antecedents)}",
                    priority_score=80,
                    expected_impact={"campaign_response": rule["confidence"] * 100},
                    action_items=[
                        f"Create targeted campaigns for {', '.join(antecedents)}",
                        f"Highlight benefits related to {', '.join(consequents)}",
                        "Use personalized messaging"
                    ],
                    success_probability=rule["confidence"],
                    cost_estimate=10000
                )
                recommendations.append(recommendation)
            
            elif action_type == "seasonal_campaign":
                recommendation = RecommendationEngine(
                    recommendation_type="seasonal_campaign",
                    target_audience=f"donors during {', '.join(antecedents)}",
                    priority_score=75,
                    expected_impact={"seasonal_increase": rule["lift"] * 20},
                    action_items=[
                        f"Plan special campaigns for {', '.join(antecedents)}",
                        "Adjust staffing levels accordingly",
                        "Prepare for increased demand"
                    ],
                    success_probability=rule["confidence"],
                    cost_estimate=15000
                )
                recommendations.append(recommendation)
            
            elif action_type == "retention_strategy":
                recommendation = RecommendationEngine(
                    recommendation_type="retention_strategy",
                    target_audience=f"donors showing {', '.join(antecedents)}",
                    priority_score=85,
                    expected_impact={"retention_improvement": rule["confidence"] * 30},
                    action_items=[
                        f"Implement retention programs for {', '.join(antecedents)}",
                        "Provide personalized engagement",
                        "Monitor loyalty metrics closely"
                    ],
                    success_probability=rule["confidence"],
                    cost_estimate=8000
                )
                recommendations.append(recommendation)
            
            elif action_type == "health_screening":
                recommendation = RecommendationEngine(
                    recommendation_type="health_screening",
                    target_audience=f"donors with {', '.join(antecedents)}",
                    priority_score=70,
                    expected_impact={"health_outcome_improvement": rule["confidence"] * 25},
                    action_items=[
                        f"Enhanced health screening for {', '.join(antecedents)}",
                        "Provide health education",
                        "Monitor health parameters"
                    ],
                    success_probability=rule["confidence"],
                    cost_estimate=5000
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_rule_summary(self, rules: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary of association rules"""
        if rules.empty:
            return {"total_rules": 0}
        
        summary = {
            "total_rules": len(rules),
            "high_confidence_rules": len(rules[rules['confidence'] >= 0.8]),
            "high_lift_rules": len(rules[rules['lift'] >= 2.0]),
            "very_high_lift_rules": len(rules[rules['lift'] >= 3.0]),
            "strong_rules": len(rules[(rules['confidence'] >= 0.8) & (rules['lift'] >= 1.5)]),
            "rule_quality_distribution": {
                "excellent": len(rules[(rules['confidence'] >= 0.9) & (rules['lift'] >= 2.0)]),
                "good": len(rules[(rules['confidence'] >= 0.7) & (rules['lift'] >= 1.5)]),
                "fair": len(rules[(rules['confidence'] >= 0.5) & (rules['lift'] >= 1.2)]),
                "poor": len(rules[(rules['confidence'] < 0.5) | (rules['lift'] < 1.2)])
            }
        }
        
        return summary
    
    def analyze_rule_impact(self, rules: pd.DataFrame, 
                          business_metrics: Dict[str, float]) -> Dict[str, Any]:
        """Analyze potential business impact of association rules"""
        impact_analysis = {
            "high_impact_rules": [],
            "roi_estimates": {},
            "implementation_priority": []
        }
        
        for _, rule in rules.iterrows():
            # Estimate business impact based on rule strength
            confidence = rule['confidence']
            lift = rule['lift']
            support = rule['support']
            
            # Simplified impact calculation
            impact_score = (confidence * lift * support) * 100
            
            if impact_score > 50:  # High impact threshold
                impact_analysis["high_impact_rules"].append({
                    "antecedents": list(rule['antecedents']),
                    "consequents": list(rule['consequents']),
                    "impact_score": impact_score,
                    "estimated_roi": impact_score * 0.5  # Simplified ROI estimate
                })
        
        # Sort by impact
        impact_analysis["high_impact_rules"].sort(
            key=lambda x: x["impact_score"], reverse=True
        )
        
        return impact_analysis
    
    def export_association_report(self, results: Dict[str, Any], 
                                filename: str = "association_analysis_report.json") -> Dict[str, Any]:
        """Export comprehensive association analysis report"""
        report = {
            "report_generated": datetime.now().isoformat(),
            "analysis_results": results,
            "metadata": {
                "total_transactions_analyzed": len(results.get("frequent_itemsets", [])),
                "algorithm_used": results.get("algorithm", "unknown"),
                "parameters": results.get("parameters", {})
            }
        }
        
        try:
            import json
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            return {"success": True, "filename": filename}
        except Exception as e:
            return {"success": False, "error": str(e)}
