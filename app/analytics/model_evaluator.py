"""
Model evaluation and performance assessment tools
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, mean_absolute_percentage_error,
    r2_score, roc_auc_score, confusion_matrix, classification_report
)
from sklearn.model_selection import cross_val_score, learning_curve, validation_curve
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class ModelEvaluator:
    """Comprehensive model evaluation and performance assessment"""
    
    def __init__(self):
        self.evaluation_history = []
        self.benchmark_scores = {
            "classification": {"accuracy": 0.8, "precision": 0.8, "recall": 0.8, "f1": 0.8},
            "regression": {"r2": 0.7, "rmse": 100, "mae": 50, "mape": 20},
            "clustering": {"silhouette": 0.5, "inertia": 1000}
        }
    
    def evaluate_classification_model(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                     y_prob: np.ndarray = None,
                                     model_name: str = "unknown") -> Dict[str, Any]:
        """Comprehensive classification model evaluation"""
        
        # Basic metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # Classification report
        class_report = classification_report(y_true, y_pred, output_dict=True)
        
        # ROC AUC if probabilities provided
        roc_auc = None
        if y_prob is not None and len(np.unique(y_true)) == 2:
            roc_auc = roc_auc_score(y_true, y_prob[:, 1])
        
        # Per-class metrics
        per_class_metrics = self._extract_per_class_metrics(class_report)
        
        # Overall assessment
        overall_score = self._calculate_classification_score(accuracy, precision, recall, f1)
        
        # Benchmark comparison
        benchmark_comparison = self._compare_to_benchmark("classification", {
            "accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1
        })
        
        evaluation_result = {
            "model_name": model_name,
            "model_type": "classification",
            "evaluation_date": datetime.now().isoformat(),
            "sample_size": len(y_true),
            "metrics": {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "roc_auc": roc_auc
            },
            "confusion_matrix": cm.tolist(),
            "classification_report": class_report,
            "per_class_metrics": per_class_metrics,
            "overall_score": overall_score,
            "benchmark_comparison": benchmark_comparison,
            "recommendations": self._generate_classification_recommendations(accuracy, precision, recall, f1)
        }
        
        self.evaluation_history.append(evaluation_result)
        return evaluation_result
    
    def evaluate_regression_model(self, y_true: np.ndarray, y_pred: np.ndarray,
                                model_name: str = "unknown") -> Dict[str, Any]:
        """Comprehensive regression model evaluation"""
        
        # Basic metrics
        r2 = r2_score(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred) * 100
        
        # Residual analysis
        residuals = y_true - y_pred
        residual_stats = {
            "mean": np.mean(residuals),
            "std": np.std(residuals),
            "skewness": stats.skew(residuals),
            "kurtosis": stats.kurtosis(residuals)
        }
        
        # Prediction intervals (simplified)
        prediction_intervals = self._calculate_prediction_intervals(y_true, y_pred)
        
        # Error distribution
        error_distribution = self._analyze_error_distribution(residuals)
        
        # Overall assessment
        overall_score = self._calculate_regression_score(r2, rmse, mae, mape)
        
        # Benchmark comparison
        benchmark_comparison = self._compare_to_benchmark("regression", {
            "r2": r2, "rmse": rmse, "mae": mae, "mape": mape
        })
        
        evaluation_result = {
            "model_name": model_name,
            "model_type": "regression",
            "evaluation_date": datetime.now().isoformat(),
            "sample_size": len(y_true),
            "metrics": {
                "r2_score": r2,
                "mse": mse,
                "rmse": rmse,
                "mae": mae,
                "mape": mape
            },
            "residual_analysis": residual_stats,
            "prediction_intervals": prediction_intervals,
            "error_distribution": error_distribution,
            "overall_score": overall_score,
            "benchmark_comparison": benchmark_comparison,
            "recommendations": self._generate_regression_recommendations(r2, rmse, mae, mape)
        }
        
        self.evaluation_history.append(evaluation_result)
        return evaluation_result
    
    def evaluate_clustering_model(self, data: np.ndarray, labels: np.ndarray,
                                model_name: str = "unknown") -> Dict[str, Any]:
        """Comprehensive clustering model evaluation"""
        
        try:
            from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
            
            # Silhouette score
            silhouette = silhouette_score(data, labels)
            
            # Calinski-Harabasz score
            calinski_harabasz = calinski_harabasz_score(data, labels)
            
            # Davies-Bouldin score
            davies_bouldin = davies_bouldin_score(data, labels)
            
            # Inertia (for K-means)
            inertia = self._calculate_inertia(data, labels)
            
            # Cluster quality analysis
            cluster_quality = self._analyze_cluster_quality(data, labels)
            
            # Overall assessment
            overall_score = self._calculate_clustering_score(silhouette, calinski_harabasz, davies_bouldin)
            
            # Benchmark comparison
            benchmark_comparison = self._compare_to_benchmark("clustering", {
                "silhouette": silhouette, "inertia": inertia
            })
            
        except ImportError:
            # Fallback if sklearn metrics not available
            silhouette = 0.5
            calinski_harabasz = 1000
            davies_bouldin = 1.0
            inertia = self._calculate_inertia(data, labels)
            cluster_quality = {}
            overall_score = 0.5
            benchmark_comparison = {}
        
        evaluation_result = {
            "model_name": model_name,
            "model_type": "clustering",
            "evaluation_date": datetime.now().isoformat(),
            "sample_size": len(data),
            "n_clusters": len(np.unique(labels)),
            "metrics": {
                "silhouette_score": silhouette,
                "calinski_harabasz_score": calinski_harabasz,
                "davies_bouldin_score": davies_bouldin,
                "inertia": inertia
            },
            "cluster_quality": cluster_quality,
            "overall_score": overall_score,
            "benchmark_comparison": benchmark_comparison,
            "recommendations": self._generate_clustering_recommendations(silhouette, davies_bouldin)
        }
        
        self.evaluation_history.append(evaluation_result)
        return evaluation_result
    
    def evaluate_forecasting_model(self, actual: np.ndarray, predicted: np.ndarray,
                                  forecast_horizon: int = 30,
                                  model_name: str = "unknown") -> Dict[str, Any]:
        """Comprehensive forecasting model evaluation"""
        
        # Basic metrics
        r2 = r2_score(actual, predicted)
        mse = mean_squared_error(actual, predicted)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(actual, predicted)
        mape = mean_absolute_percentage_error(actual, predicted) * 100
        
        # Forecast-specific metrics
        directional_accuracy = self._calculate_directional_accuracy(actual, predicted)
        bias = np.mean(predicted - actual)
        
        # Time series specific analysis
        ts_analysis = self._analyze_time_series_performance(actual, predicted)
        
        # Forecast accuracy by horizon
        horizon_accuracy = self._analyze_forecast_horizon_accuracy(actual, predicted, forecast_horizon)
        
        # Overall assessment
        overall_score = self._calculate_forecasting_score(r2, rmse, mape, directional_accuracy)
        
        # Benchmark comparison
        benchmark_comparison = self._compare_to_benchmark("regression", {
            "r2": r2, "rmse": rmse, "mape": mape
        })
        
        evaluation_result = {
            "model_name": model_name,
            "model_type": "forecasting",
            "evaluation_date": datetime.now().isoformat(),
            "sample_size": len(actual),
            "forecast_horizon": forecast_horizon,
            "metrics": {
                "r2_score": r2,
                "mse": mse,
                "rmse": rmse,
                "mae": mae,
                "mape": mape,
                "directional_accuracy": directional_accuracy,
                "bias": bias
            },
            "time_series_analysis": ts_analysis,
            "horizon_accuracy": horizon_accuracy,
            "overall_score": overall_score,
            "benchmark_comparison": benchmark_comparison,
            "recommendations": self._generate_forecasting_recommendations(r2, mape, directional_accuracy)
        }
        
        self.evaluation_history.append(evaluation_result)
        return evaluation_result
    
    def compare_models(self, model_evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple models and recommend the best"""
        if not model_evaluations:
            return {"error": "No model evaluations provided"}
        
        # Group evaluations by model type
        model_types = {}
        for evaluation in model_evaluations:
            model_type = evaluation.get("model_type", "unknown")
            if model_type not in model_types:
                model_types[model_type] = []
            model_types[model_type].append(evaluation)
        
        comparison_results = {}
        
        for model_type, evaluations in model_types.items():
            comparison_results[model_type] = self._compare_models_by_type(evaluations)
        
        # Overall best model
        best_model = self._find_best_overall_model(model_evaluations)
        
        # Model ranking
        model_ranking = self._rank_models(model_evaluations)
        
        return {
            "model_type_comparisons": comparison_results,
            "best_overall_model": best_model,
            "model_ranking": model_ranking,
            "comparison_summary": self._generate_comparison_summary(model_evaluations),
            "recommendations": self._generate_comparison_recommendations(model_evaluations)
        }
    
    def _extract_per_class_metrics(self, class_report: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Extract per-class metrics from classification report"""
        per_class = {}
        
        for key, value in class_report.items():
            if key not in ["accuracy", "macro avg", "weighted avg"]:
                if isinstance(value, dict):
                    per_class[key] = {
                        "precision": value.get("precision", 0),
                        "recall": value.get("recall", 0),
                        "f1-score": value.get("f1-score", 0),
                        "support": value.get("support", 0)
                    }
        
        return per_class
    
    def _calculate_classification_score(self, accuracy: float, precision: float, 
                                       recall: float, f1: float) -> float:
        """Calculate overall classification score"""
        return (accuracy + precision + recall + f1) / 4
    
    def _calculate_regression_score(self, r2: float, rmse: float, mae: float, mape: float) -> float:
        """Calculate overall regression score"""
        # Normalize metrics (higher is better for all)
        r2_score = max(0, r2)  # R² can be negative
        rmse_score = 1 / (1 + rmse / 100)  # Normalize RMSE
        mae_score = 1 / (1 + mae / 50)    # Normalize MAE
        mape_score = 1 / (1 + mape / 20)  # Normalize MAPE
        
        return (r2_score + rmse_score + mae_score + mape_score) / 4
    
    def _calculate_clustering_score(self, silhouette: float, calinski_harabasz: float, 
                                  davies_bouldin: float) -> float:
        """Calculate overall clustering score"""
        # Normalize metrics
        silhouette_score = silhouette  # Already 0-1
        ch_score = min(1, calinski_harabasz / 1000)  # Normalize Calinski-Harabasz
        db_score = 1 / (1 + davies_bouldin)  # Invert Davies-Bouldin (lower is better)
        
        return (silhouette_score + ch_score + db_score) / 3
    
    def _calculate_forecasting_score(self, r2: float, rmse: float, mape: float, 
                                   directional_accuracy: float) -> float:
        """Calculate overall forecasting score"""
        r2_score = max(0, r2)
        rmse_score = 1 / (1 + rmse / 100)
        mape_score = 1 / (1 + mape / 20)
        da_score = directional_accuracy / 100
        
        return (r2_score + rmse_score + mape_score + da_score) / 4
    
    def _compare_to_benchmark(self, model_type: str, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Compare model performance to benchmarks"""
        benchmark = self.benchmark_scores.get(model_type, {})
        comparison = {}
        
        for metric, value in metrics.items():
            if metric in benchmark:
                benchmark_value = benchmark[metric]
                if metric in ["r2", "accuracy", "precision", "recall", "f1", "silhouette"]:
                    # Higher is better
                    performance = "above" if value > benchmark_value else "below"
                    percentage_diff = ((value - benchmark_value) / benchmark_value) * 100
                else:
                    # Lower is better
                    performance = "above" if value < benchmark_value else "below"
                    percentage_diff = ((benchmark_value - value) / benchmark_value) * 100
                
                comparison[metric] = {
                    "model_value": value,
                    "benchmark_value": benchmark_value,
                    "performance": performance,
                    "percentage_difference": percentage_diff
                }
        
        return comparison
    
    def _calculate_prediction_intervals(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Calculate prediction intervals"""
        residuals = y_true - y_pred
        std_residual = np.std(residuals)
        
        # 95% prediction interval
        margin_of_error = 1.96 * std_residual
        
        return {
            "margin_of_error_95": margin_of_error,
            "interval_width": 2 * margin_of_error,
            "coverage_rate": np.mean(np.abs(residuals) <= margin_of_error)
        }
    
    def _analyze_error_distribution(self, residuals: np.ndarray) -> Dict[str, Any]:
        """Analyze error distribution"""
        return {
            "is_normal": stats.normaltest(residuals)[1] > 0.05,
            "skewness": stats.skew(residuals),
            "kurtosis": stats.kurtosis(residuals),
            "outliers": np.sum(np.abs(residuals) > 2 * np.std(residuals)),
            "outlier_percentage": np.sum(np.abs(residuals) > 2 * np.std(residuals)) / len(residuals) * 100
        }
    
    def _calculate_inertia(self, data: np.ndarray, labels: np.ndarray) -> float:
        """Calculate inertia for clustering evaluation"""
        inertia = 0.0
        for cluster_id in np.unique(labels):
            cluster_points = data[labels == cluster_id]
            centroid = cluster_points.mean(axis=0)
            inertia += np.sum((cluster_points - centroid) ** 2)
        return inertia
    
    def _analyze_cluster_quality(self, data: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
        """Analyze cluster quality metrics"""
        cluster_sizes = [np.sum(labels == cluster_id) for cluster_id in np.unique(labels)]
        
        return {
            "cluster_sizes": cluster_sizes,
            "size_balance": np.std(cluster_sizes) / np.mean(cluster_sizes) if np.mean(cluster_sizes) > 0 else 0,
            "smallest_cluster": min(cluster_sizes),
            "largest_cluster": max(cluster_sizes),
            "size_ratio": max(cluster_sizes) / min(cluster_sizes) if min(cluster_sizes) > 0 else float('inf')
        }
    
    def _calculate_directional_accuracy(self, actual: np.ndarray, predicted: np.ndarray) -> float:
        """Calculate directional accuracy for time series"""
        if len(actual) < 2:
            return 0.0
        
        actual_direction = np.diff(actual) > 0
        predicted_direction = np.diff(predicted) > 0
        
        return np.mean(actual_direction == predicted_direction) * 100
    
    def _analyze_time_series_performance(self, actual: np.ndarray, predicted: np.ndarray) -> Dict[str, Any]:
        """Analyze time series specific performance"""
        # Autocorrelation of residuals
        residuals = actual - predicted
        if len(residuals) > 1:
            autocorr_lag1 = np.corrcoef(residuals[:-1], residuals[1:])[0, 1]
        else:
            autocorr_lag1 = 0.0
        
        return {
            "residual_autocorrelation_lag1": autocorr_lag1,
            "mean_absolute_percentage_error": mean_absolute_percentage_error(actual, predicted) * 100,
            "trend_accuracy": self._calculate_trend_accuracy(actual, predicted)
        }
    
    def _calculate_trend_accuracy(self, actual: np.ndarray, predicted: np.ndarray) -> float:
        """Calculate trend accuracy"""
        if len(actual) < 3:
            return 0.0
        
        # Calculate trends (moving average)
        window = min(3, len(actual) // 2)
        actual_trend = np.convolve(actual, np.ones(window)/window, mode='valid')
        predicted_trend = np.convolve(predicted, np.ones(window)/window, mode='valid')
        
        if len(actual_trend) < 2:
            return 0.0
        
        actual_direction = np.diff(actual_trend) > 0
        predicted_direction = np.diff(predicted_trend) > 0
        
        return np.mean(actual_direction == predicted_direction) * 100
    
    def _analyze_forecast_horizon_accuracy(self, actual: np.ndarray, predicted: np.ndarray, 
                                         horizon: int) -> Dict[str, float]:
        """Analyze accuracy by forecast horizon"""
        horizon_accuracies = {}
        
        # Divide forecast into segments
        segment_size = len(actual) // max(1, horizon // 5)  # 5 segments max
        
        for i in range(0, len(actual), segment_size):
            end_idx = min(i + segment_size, len(actual))
            if end_idx > i:
                segment_actual = actual[i:end_idx]
                segment_predicted = predicted[i:end_idx]
                
                segment_mape = mean_absolute_percentage_error(segment_actual, segment_predicted) * 100
                horizon_accuracies[f"segment_{i//segment_size + 1}"] = segment_mape
        
        return horizon_accuracies
    
    def _compare_models_by_type(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare models of the same type"""
        if not evaluations:
            return {}
        
        # Sort by overall score
        sorted_evaluations = sorted(evaluations, key=lambda x: x.get("overall_score", 0), reverse=True)
        
        best_model = sorted_evaluations[0]
        worst_model = sorted_evaluations[-1]
        
        # Calculate average performance
        avg_score = np.mean([eval.get("overall_score", 0) for eval in evaluations])
        
        return {
            "best_model": best_model.get("model_name", "unknown"),
            "best_score": best_model.get("overall_score", 0),
            "worst_model": worst_model.get("model_name", "unknown"),
            "worst_score": worst_model.get("overall_score", 0),
            "average_score": avg_score,
            "model_count": len(evaluations),
            "score_range": best_model.get("overall_score", 0) - worst_model.get("overall_score", 0)
        }
    
    def _find_best_overall_model(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find the best overall model across all types"""
        if not evaluations:
            return {}
        
        best_evaluation = max(evaluations, key=lambda x: x.get("overall_score", 0))
        
        return {
            "model_name": best_evaluation.get("model_name", "unknown"),
            "model_type": best_evaluation.get("model_type", "unknown"),
            "overall_score": best_evaluation.get("overall_score", 0),
            "key_metrics": best_evaluation.get("metrics", {})
        }
    
    def _rank_models(self, evaluations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank models by performance"""
        return sorted(evaluations, key=lambda x: x.get("overall_score", 0), reverse=True)
    
    def _generate_comparison_summary(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of model comparisons"""
        model_types = set(eval.get("model_type", "unknown") for eval in evaluations)
        
        summary = {
            "total_models": len(evaluations),
            "model_types": list(model_types),
            "best_by_type": {},
            "performance_distribution": {
                "excellent": 0,  # > 0.9
                "good": 0,        # 0.7-0.9
                "fair": 0,        # 0.5-0.7
                "poor": 0         # < 0.5
            }
        }
        
        # Best model by type
        for model_type in model_types:
            type_evaluations = [eval for eval in evaluations if eval.get("model_type") == model_type]
            if type_evaluations:
                best = max(type_evaluations, key=lambda x: x.get("overall_score", 0))
                summary["best_by_type"][model_type] = best.get("model_name", "unknown")
        
        # Performance distribution
        for eval in evaluations:
            score = eval.get("overall_score", 0)
            if score > 0.9:
                summary["performance_distribution"]["excellent"] += 1
            elif score > 0.7:
                summary["performance_distribution"]["good"] += 1
            elif score > 0.5:
                summary["performance_distribution"]["fair"] += 1
            else:
                summary["performance_distribution"]["poor"] += 1
        
        return summary
    
    def _generate_classification_recommendations(self, accuracy: float, precision: float, 
                                              recall: float, f1: float) -> List[str]:
        """Generate recommendations for classification models"""
        recommendations = []
        
        if accuracy < 0.7:
            recommendations.append("Consider feature engineering to improve accuracy")
        
        if precision < 0.7:
            recommendations.append("Model has high false positive rate - adjust decision threshold")
        
        if recall < 0.7:
            recommendations.append("Model has high false negative rate - consider different algorithm")
        
        if f1 < 0.7:
            recommendations.append("Balance between precision and recall needs improvement")
        
        if all(metric > 0.85 for metric in [accuracy, precision, recall, f1]):
            recommendations.append("Excellent performance - consider model deployment")
        
        return recommendations
    
    def _generate_regression_recommendations(self, r2: float, rmse: float, mae: float, mape: float) -> List[str]:
        """Generate recommendations for regression models"""
        recommendations = []
        
        if r2 < 0.5:
            recommendations.append("Low R² score - consider adding more features or different model")
        
        if rmse > 100:
            recommendations.append("High RMSE - check for outliers and data quality")
        
        if mae > 50:
            recommendations.append("High MAE - consider non-linear models")
        
        if mape > 30:
            recommendations.append("High MAPE - model struggles with relative errors")
        
        if r2 > 0.8 and rmse < 50:
            recommendations.append("Good regression performance - ready for deployment")
        
        return recommendations
    
    def _generate_clustering_recommendations(self, silhouette: float, davies_bouldin: float) -> List[str]:
        """Generate recommendations for clustering models"""
        recommendations = []
        
        if silhouette < 0.3:
            recommendations.append("Low silhouette score - clusters may not be well-separated")
        
        if davies_bouldin > 1.5:
            recommendations.append("High Davies-Bouldin score - consider different number of clusters")
        
        if silhouette > 0.7 and davies_bouldin < 0.5:
            recommendations.append("Excellent clustering quality - results are reliable")
        
        return recommendations
    
    def _generate_forecasting_recommendations(self, r2: float, mape: float, directional_accuracy: float) -> List[str]:
        """Generate recommendations for forecasting models"""
        recommendations = []
        
        if r2 < 0.5:
            recommendations.append("Low R² - consider more sophisticated time series models")
        
        if mape > 25:
            recommendations.append("High MAPE - model struggles with percentage accuracy")
        
        if directional_accuracy < 60:
            recommendations.append("Poor directional accuracy - consider trend-focused models")
        
        if r2 > 0.8 and mape < 15:
            recommendations.append("Good forecasting performance - suitable for operational use")
        
        return recommendations
    
    def _generate_comparison_recommendations(self, evaluations: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on model comparison"""
        recommendations = []
        
        if len(evaluations) < 2:
            recommendations.append("Consider training multiple models for comparison")
            return recommendations
        
        scores = [eval.get("overall_score", 0) for eval in evaluations]
        max_score = max(scores)
        min_score = min(scores)
        
        if max_score - min_score > 0.3:
            recommendations.append("Significant performance difference - use best performing model")
        else:
            recommendations.append("Models have similar performance - consider complexity and interpretability")
        
        # Check for overfitting
        high_scores = [score for score in scores if score > 0.95]
        if len(high_scores) > 0:
            recommendations.append("Very high scores detected - validate for potential overfitting")
        
        return recommendations
    
    def get_evaluation_history(self) -> List[Dict[str, Any]]:
        """Get all evaluation history"""
        return self.evaluation_history.copy()
    
    def clear_evaluation_history(self) -> None:
        """Clear evaluation history"""
        self.evaluation_history.clear()
    
    def export_evaluation_report(self, filename: str = "model_evaluation_report.json") -> Dict[str, Any]:
        """Export comprehensive evaluation report"""
        report = {
            "report_generated": datetime.now().isoformat(),
            "total_evaluations": len(self.evaluation_history),
            "evaluation_history": self.evaluation_history,
            "benchmark_scores": self.benchmark_scores,
            "summary": self._generate_comparison_summary(self.evaluation_history)
        }
        
        try:
            import json
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            return {"success": True, "filename": filename}
        except Exception as e:
            return {"success": False, "error": str(e)}
