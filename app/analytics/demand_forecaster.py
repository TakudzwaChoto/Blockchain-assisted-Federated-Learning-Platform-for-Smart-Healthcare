"""
Blood demand forecasting engine with multiple algorithms
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
import warnings
warnings.filterwarnings('ignore')

# Statistical models
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from scipy import stats

# Machine learning models
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score

# Deep learning (TensorFlow/Keras)
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.optimizers import Adam
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

# Prophet for time series forecasting
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False

from ..models.analytics import DemandForecast, TimeGranularity
from ..config import Config

class DemandForecaster:
    """Advanced demand forecasting with multiple algorithms"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_columns = []
        
    def forecast_demand(self, data: pd.DataFrame, 
                       forecast_horizon_days: int = 30,
                       model_types: List[str] = None,
                       granularity: str = "daily",
                       target_variable: str = "volume_ml") -> Dict[str, DemandForecast]:
        """Generate demand forecasts using multiple models"""
        if model_types is None:
            model_types = ["arima", "linear_regression"]
            if PROPHET_AVAILABLE:
                model_types.append("prophet")
            if TENSORFLOW_AVAILABLE:
                model_types.append("lstm")
        
        # Prepare data
        prepared_data = self._prepare_forecasting_data(data, target_variable, granularity)
        
        results = {}
        
        for model_type in model_types:
            try:
                forecast = self._train_and_forecast(
                    prepared_data, model_type, forecast_horizon_days, 
                    granularity, target_variable
                )
                results[model_type] = forecast
            except Exception as e:
                print(f"Error training {model_type} model: {str(e)}")
                continue
        
        return results
    
    def _prepare_forecasting_data(self, data: pd.DataFrame, target_variable: str, 
                                granularity: str) -> pd.DataFrame:
        """Prepare data for time series forecasting"""
        # Ensure we have date column
        if "donation_date" not in data.columns:
            raise ValueError("Data must contain 'donation_date' column")
        
        # Convert dates
        data["donation_date"] = pd.to_datetime(data["donation_date"])
        
        # Aggregate by time period
        if granularity == "daily":
            data["period"] = data["donation_date"].dt.date
        elif granularity == "weekly":
            data["period"] = data["donation_date"].dt.to_period('W').dt.start_time
        elif granularity == "monthly":
            data["period"] = data["donation_date"].dt.to_period('M').dt.start_time
        elif granularity == "quarterly":
            data["period"] = data["donation_date"].dt.to_period('Q').dt.start_time
        else:
            data["period"] = data["donation_date"].dt.to_period('M').dt.start_time
        
        # Aggregate target variable
        if target_variable in data.columns:
            aggregated = data.groupby("period")[target_variable].sum().reset_index()
        else:
            # If target variable not found, use count as default
            aggregated = data.groupby("period").size().reset_index(name=target_variable)
        
        # Rename columns for consistency
        aggregated.columns = ["ds", "y"]
        aggregated = aggregated.sort_values("ds").reset_index(drop=True)
        
        # Add time-based features
        aggregated = self._add_time_features(aggregated)
        
        return aggregated
    
    def _add_time_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add time-based features for machine learning models"""
        data["year"] = data["ds"].dt.year
        data["month"] = data["ds"].dt.month
        data["quarter"] = data["ds"].dt.quarter
        data["week_of_year"] = data["ds"].dt.isocalendar().week
        data["day_of_year"] = data["ds"].dt.dayofyear
        data["day_of_week"] = data["ds"].dt.dayofweek
        data["is_weekend"] = (data["ds"].dt.dayofweek >= 5).astype(int)
        
        # Cyclical features
        data["month_sin"] = np.sin(2 * np.pi * data["month"] / 12)
        data["month_cos"] = np.cos(2 * np.pi * data["month"] / 12)
        data["day_sin"] = np.sin(2 * np.pi * data["ds"].dt.day / 31)
        data["day_cos"] = np.cos(2 * np.pi * data["ds"].dt.day / 31)
        
        return data
    
    def _train_and_forecast(self, data: pd.DataFrame, model_type: str, 
                          forecast_horizon_days: int, granularity: str, 
                          target_variable: str) -> DemandForecast:
        """Train specific model and generate forecast"""
        
        if model_type == "arima":
            return self._arima_forecast(data, forecast_horizon_days, granularity, target_variable)
        elif model_type == "prophet":
            return self._prophet_forecast(data, forecast_horizon_days, granularity, target_variable)
        elif model_type == "lstm":
            return self._lstm_forecast(data, forecast_horizon_days, granularity, target_variable)
        elif model_type == "linear_regression":
            return self._linear_regression_forecast(data, forecast_horizon_days, granularity, target_variable)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def _arima_forecast(self, data: pd.DataFrame, forecast_horizon_days: int, 
                       granularity: str, target_variable: str) -> DemandForecast:
        """ARIMA time series forecasting"""
        # Prepare time series data
        ts_data = data.set_index("ds")["y"]
        
        # Check for stationarity
        adf_result = adfuller(ts_data.dropna())
        is_stationary = adf_result[1] < 0.05
        
        # Determine ARIMA parameters (simplified)
        if is_stationary:
            order = (1, 0, 1)
        else:
            order = (1, 1, 1)
        
        # Fit ARIMA model
        model = ARIMA(ts_data, order=order)
        fitted_model = model.fit()
        
        # Generate forecast
        forecast_steps = self._get_forecast_steps(forecast_horizon_days, granularity)
        forecast_result = fitted_model.forecast(steps=forecast_steps)
        forecast_ci = fitted_model.get_forecast(steps=forecast_steps).conf_int()
        
        # Calculate performance metrics
        train_predictions = fitted_model.fittedvalues
        actual_values = ts_data.iloc[len(train_predictions) - len(train_predictions):]
        
        performance = self._calculate_model_performance(actual_values, train_predictions[-len(actual_values):])
        
        # Format forecast values
        forecast_values = []
        confidence_intervals = []
        
        last_date = data["ds"].max()
        date_increment = self._get_date_increment(granularity)
        
        for i, value in enumerate(forecast_result):
            forecast_date = last_date + timedelta(days=i * date_increment)
            forecast_values.append({
                "date": forecast_date.isoformat(),
                "value": float(value)
            })
            
            if i < len(forecast_ci):
                confidence_intervals.append((
                    float(forecast_ci.iloc[i, 0]),
                    float(forecast_ci.iloc[i, 1])
                ))
        
        return DemandForecast(
            model_type="arima",
            target_variable=target_variable,
            forecast_horizon_days=forecast_horizon_days,
            granularity=TimeGranularity(granularity),
            training_data_period_days=len(data) * self._get_date_increment(granularity),
            forecast_values=forecast_values,
            confidence_intervals=confidence_intervals,
            model_performance=performance,
            last_training_date=datetime.now(),
            accuracy_score=performance.get("r2", 0)
        )
    
    def _prophet_forecast(self, data: pd.DataFrame, forecast_horizon_days: int, 
                         granularity: str, target_variable: str) -> DemandForecast:
        """Prophet time series forecasting"""
        if not PROPHET_AVAILABLE:
            raise ImportError("Prophet is not installed")
        
        # Prepare data for Prophet
        prophet_data = data[["ds", "y"]].copy()
        
        # Create and fit Prophet model
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=granularity == "daily",
            changepoint_prior_scale=0.05
        )
        
        model.fit(prophet_data)
        
        # Create future dataframe
        forecast_steps = self._get_forecast_steps(forecast_horizon_days, granularity)
        future = model.make_future_dataframe(periods=forecast_steps, freq=self._get_prophet_freq(granularity))
        
        # Generate forecast
        forecast = model.predict(future)
        
        # Extract forecast values
        forecast_values = []
        confidence_intervals = []
        
        # Get only future predictions
        future_forecast = forecast.iloc[-forecast_steps:]
        
        for _, row in future_forecast.iterrows():
            forecast_values.append({
                "date": row["ds"].isoformat(),
                "value": float(row["yhat"])
            })
            confidence_intervals.append((
                float(row["yhat_lower"]),
                float(row["yhat_upper"])
            ))
        
        # Calculate performance metrics
        train_forecast = forecast.iloc[:-forecast_steps]
        actual_values = data["y"].values
        predicted_values = train_forecast["yhat"].values[-len(actual_values):]
        
        performance = self._calculate_model_performance(actual_values, predicted_values)
        
        return DemandForecast(
            model_type="prophet",
            target_variable=target_variable,
            forecast_horizon_days=forecast_horizon_days,
            granularity=TimeGranularity(granularity),
            training_data_period_days=len(data) * self._get_date_increment(granularity),
            forecast_values=forecast_values,
            confidence_intervals=confidence_intervals,
            model_performance=performance,
            last_training_date=datetime.now(),
            accuracy_score=performance.get("r2", 0)
        )
    
    def _lstm_forecast(self, data: pd.DataFrame, forecast_horizon_days: int, 
                      granularity: str, target_variable: str) -> DemandForecast:
        """LSTM neural network forecasting"""
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is not installed")
        
        # Prepare data for LSTM
        feature_cols = ["month", "quarter", "week_of_year", "day_of_week", 
                       "is_weekend", "month_sin", "month_cos", "day_sin", "day_cos"]
        
        # Scale features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(data[feature_cols])
        scaled_target = scaler.fit_transform(data[["y"]])
        
        # Create sequences
        sequence_length = min(30, len(data) // 3)  # Use 30 periods or 1/3 of data
        X, y = self._create_sequences(scaled_features, scaled_target, sequence_length)
        
        # Build LSTM model
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(sequence_length, len(feature_cols))),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        
        # Train model
        model.fit(X, y, epochs=50, batch_size=32, verbose=0)
        
        # Generate forecasts
        forecast_values = []
        confidence_intervals = []
        
        # Start with last sequence
        last_sequence = X[-1]
        current_sequence = last_sequence.copy()
        
        for i in range(self._get_forecast_steps(forecast_horizon_days, granularity)):
            # Predict next value
            prediction = model.predict(current_sequence.reshape(1, sequence_length, len(feature_cols)), verbose=0)
            
            # Inverse transform to get actual value
            actual_prediction = scaler.inverse_transform(prediction)[0, 0]
            
            # Calculate confidence interval (simplified)
            confidence = actual_prediction * 0.1  # 10% confidence band
            confidence_intervals.append((actual_prediction - confidence, actual_prediction + confidence))
            
            # Add to forecast values
            forecast_date = data["ds"].max() + timedelta(days=i * self._get_date_increment(granularity))
            forecast_values.append({
                "date": forecast_date.isoformat(),
                "value": float(actual_prediction)
            })
            
            # Update sequence for next prediction (simplified)
            current_sequence = np.roll(current_sequence, -1, axis=0)
            # This is a simplified approach - in practice, you'd need to update features properly
        
        # Calculate performance metrics
        train_predictions = model.predict(X, verbose=0)
        train_predictions_actual = scaler.inverse_transform(train_predictions).flatten()
        actual_values = data["y"].values[sequence_length:]
        
        performance = self._calculate_model_performance(actual_values, train_predictions_actual)
        
        return DemandForecast(
            model_type="lstm",
            target_variable=target_variable,
            forecast_horizon_days=forecast_horizon_days,
            granularity=TimeGranularity(granularity),
            training_data_period_days=len(data) * self._get_date_increment(granularity),
            forecast_values=forecast_values,
            confidence_intervals=confidence_intervals,
            model_performance=performance,
            last_training_date=datetime.now(),
            accuracy_score=performance.get("r2", 0)
        )
    
    def _linear_regression_forecast(self, data: pd.DataFrame, forecast_horizon_days: int, 
                                   granularity: str, target_variable: str) -> DemandForecast:
        """Linear regression forecasting with time features"""
        # Prepare features
        feature_cols = ["year", "month", "quarter", "week_of_year", "day_of_year", 
                       "day_of_week", "is_weekend", "month_sin", "month_cos", "day_sin", "day_cos"]
        
        X = data[feature_cols]
        y = data["y"]
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train model
        model = LinearRegression()
        model.fit(X_scaled, y)
        
        # Create future features
        forecast_steps = self._get_forecast_steps(forecast_horizon_days, granularity)
        future_dates = []
        future_features = []
        
        last_date = data["ds"].max()
        date_increment = self._get_date_increment(granularity)
        
        for i in range(forecast_steps):
            future_date = last_date + timedelta(days=i * date_increment)
            future_dates.append(future_date)
            
            # Create features for future date
            features = [
                future_date.year,
                future_date.month,
                future_date.quarter,
                future_date.isocalendar().week,
                future_date.dayofyear,
                future_date.dayofweek,
                1 if future_date.dayofweek >= 5 else 0,
                np.sin(2 * np.pi * future_date.month / 12),
                np.cos(2 * np.pi * future_date.month / 12),
                np.sin(2 * np.pi * future_date.day / 31),
                np.cos(2 * np.pi * future_date.day / 31)
            ]
            future_features.append(features)
        
        # Generate predictions
        future_features_scaled = scaler.transform(future_features)
        predictions = model.predict(future_features_scaled)
        
        # Format forecast values
        forecast_values = []
        confidence_intervals = []
        
        train_predictions = model.predict(X_scaled)
        residuals = y - train_predictions
        std_error = np.std(residuals)
        
        for i, (date, prediction) in enumerate(zip(future_dates, predictions)):
            forecast_values.append({
                "date": date.isoformat(),
                "value": float(prediction)
            })
            
            # Calculate confidence interval (95%)
            confidence = 1.96 * std_error
            confidence_intervals.append((
                float(prediction - confidence),
                float(prediction + confidence)
            ))
        
        # Calculate performance metrics
        performance = self._calculate_model_performance(y, train_predictions)
        
        # Feature importance
        feature_importance = dict(zip(feature_cols, np.abs(model.coef_)))
        
        return DemandForecast(
            model_type="linear_regression",
            target_variable=target_variable,
            forecast_horizon_days=forecast_horizon_days,
            granularity=TimeGranularity(granularity),
            training_data_period_days=len(data) * self._get_date_increment(granularity),
            forecast_values=forecast_values,
            confidence_intervals=confidence_intervals,
            model_performance=performance,
            feature_importance=feature_importance,
            last_training_date=datetime.now(),
            accuracy_score=performance.get("r2", 0)
        )
    
    def _create_sequences(self, features: np.ndarray, target: np.ndarray, 
                         sequence_length: int) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for LSTM training"""
        X, y = [], []
        
        for i in range(sequence_length, len(features)):
            X.append(features[i-sequence_length:i])
            y.append(target[i])
        
        return np.array(X), np.array(y)
    
    def _calculate_model_performance(self, actual: np.ndarray, predicted: np.ndarray) -> Dict[str, float]:
        """Calculate model performance metrics"""
        # Remove any NaN values
        mask = ~(np.isnan(actual) | np.isnan(predicted))
        actual_clean = actual[mask]
        predicted_clean = predicted[mask]
        
        if len(actual_clean) == 0:
            return {"r2": 0.0, "rmse": 0.0, "mape": 100.0}
        
        r2 = r2_score(actual_clean, predicted_clean)
        rmse = np.sqrt(mean_squared_error(actual_clean, predicted_clean))
        
        # Calculate MAPE (avoid division by zero)
        mape = np.mean(np.abs((actual_clean - predicted_clean) / np.maximum(actual_clean, 1e-8))) * 100
        
        return {
            "r2": r2,
            "rmse": rmse,
            "mape": mape
        }
    
    def _get_forecast_steps(self, forecast_horizon_days: int, granularity: str) -> int:
        """Convert forecast horizon to number of steps"""
        if granularity == "daily":
            return forecast_horizon_days
        elif granularity == "weekly":
            return max(1, forecast_horizon_days // 7)
        elif granularity == "monthly":
            return max(1, forecast_horizon_days // 30)
        elif granularity == "quarterly":
            return max(1, forecast_horizon_days // 90)
        else:
            return forecast_horizon_days
    
    def _get_date_increment(self, granularity: str) -> int:
        """Get date increment in days for granularity"""
        increments = {
            "daily": 1,
            "weekly": 7,
            "monthly": 30,
            "quarterly": 90
        }
        return increments.get(granularity, 1)
    
    def _get_prophet_freq(self, granularity: str) -> str:
        """Get Prophet frequency string"""
        freq_map = {
            "daily": "D",
            "weekly": "W",
            "monthly": "M",
            "quarterly": "Q"
        }
        return freq_map.get(granularity, "D")
    
    def compare_forecasts(self, forecasts: Dict[str, DemandForecast]) -> Dict[str, Any]:
        """Compare multiple forecast models and select the best"""
        if not forecasts:
            return {"error": "No forecasts to compare"}
        
        # Calculate comparison metrics
        comparison = {
            "model_count": len(forecasts),
            "models": {},
            "best_model": None,
            "best_accuracy": 0
        }
        
        for model_name, forecast in forecasts.items():
            accuracy = forecast.accuracy_score
            comparison["models"][model_name] = {
                "accuracy_score": accuracy,
                "rmse": forecast.model_performance.get("rmse", 0),
                "mape": forecast.model_performance.get("mape", 100),
                "forecast_horizon": forecast.forecast_horizon_days,
                "training_data_period": forecast.training_data_period_days
            }
            
            if accuracy > comparison["best_accuracy"]:
                comparison["best_accuracy"] = accuracy
                comparison["best_model"] = model_name
        
        # Generate ensemble forecast (simple average)
        if len(forecasts) > 1:
            ensemble_forecast = self._create_ensemble_forecast(forecasts)
            comparison["ensemble_forecast"] = ensemble_forecast
        
        return comparison
    
    def _create_ensemble_forecast(self, forecasts: Dict[str, DemandForecast]) -> Dict[str, Any]:
        """Create ensemble forecast from multiple models"""
        # Get the forecast with the most points as reference
        reference_forecast = max(forecasts.values(), key=lambda f: len(f.forecast_values))
        
        ensemble_values = []
        
        for i in range(len(reference_forecast.forecast_values)):
            date = reference_forecast.forecast_values[i]["date"]
            
            # Collect predictions from all models for this date
            predictions = []
            for forecast in forecasts.values():
                if i < len(forecast.forecast_values) and forecast.forecast_values[i]["date"] == date:
                    predictions.append(forecast.forecast_values[i]["value"])
            
            if predictions:
                ensemble_value = np.mean(predictions)
                ensemble_values.append({
                    "date": date,
                    "value": float(ensemble_value),
                    "model_count": len(predictions),
                    "std_dev": float(np.std(predictions))
                })
        
        return {
            "ensemble_values": ensemble_values,
            "method": "simple_average",
            "component_models": list(forecasts.keys())
        }
