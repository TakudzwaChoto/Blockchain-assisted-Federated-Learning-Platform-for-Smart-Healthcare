"""FastAPI backend for Blood Domain Engine."""

from __future__ import annotations

import io
import os
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .analytics.trend_analyzer import TrendAnalyzer
from .analytics.demand_forecaster import DemandForecaster
from .data_processing.batch_processor import BatchDataProcessor
from .data_mining.pattern_mining import PatternMiningEngine
from .data_mining.association_analyzer import AssociationAnalyzer


DATASETS: Dict[str, pd.DataFrame] = {}


def _ensure_upload_dir() -> str:
    upload_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
    upload_dir = os.path.abspath(upload_dir)
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir


app = FastAPI(title="Blood Domain Engine API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    dataset_id: str
    granularity: str = "monthly"
    time_period_days: int = 365


class ForecastRequest(BaseModel):
    dataset_id: str
    forecast_horizon_days: int = 30
    granularity: str = "daily"
    target_variable: str = "volume_ml"
    model_types: Optional[list[str]] = None


class MiningRequest(BaseModel):
    dataset_id: str
    pattern_types: Optional[list[str]] = None


class AssociationRequest(BaseModel):
    dataset_id: str
    min_support: float = 0.1
    min_confidence: float = 0.7
    min_lift: float = 1.0
    algorithm: str = "apriori"


@app.get("/api/v1/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "time": datetime.now().isoformat()}


@app.post("/api/v1/datasets/upload")
async def upload_dataset(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload CSV/Excel/JSON and register it as an in-memory dataset."""
    filename = file.filename or "upload"
    ext = filename.split(".")[-1].lower() if "." in filename else ""

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    # Parse into DataFrame
    try:
        if ext in ("csv", "tsv"):
            df = pd.read_csv(io.BytesIO(content))
        elif ext in ("xlsx", "xls", "xlsm"):
            df = pd.read_excel(io.BytesIO(content))
        elif ext in ("json", "jsonl", "ndjson"):
            df = pd.read_json(io.BytesIO(content), lines=ext in ("jsonl", "ndjson"))
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file extension: {ext}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    # Normalize column names
    df.columns = [str(c).strip() for c in df.columns]

    dataset_id = str(uuid4())
    DATASETS[dataset_id] = df

    # Persist the raw upload to disk (optional, for re-use)
    upload_dir = _ensure_upload_dir()
    raw_path = os.path.join(upload_dir, f"{dataset_id}_{filename}")
    try:
        with open(raw_path, "wb") as f:
            f.write(content)
    except Exception:
        pass

    return {
        "dataset_id": dataset_id,
        "filename": filename,
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "columns": df.columns.tolist(),
    }


@app.get("/api/v1/datasets/{dataset_id}")
def get_dataset_info(dataset_id: str) -> Dict[str, Any]:
    df = DATASETS.get(dataset_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return {
        "dataset_id": dataset_id,
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "columns": df.columns.tolist(),
        "preview": df.head(20).to_dict(orient="records"),
    }


@app.post("/api/v1/process")
async def process_dataset(payload: Dict[str, Any]) -> Dict[str, Any]:
    dataset_id = payload.get("dataset_id")
    if not dataset_id:
        raise HTTPException(status_code=400, detail="dataset_id is required")

    df = DATASETS.get(dataset_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    processor = BatchDataProcessor()
    processed_df, stats = await processor._process_dataset(df)  # uses cleaner/transformer/validator
    DATASETS[dataset_id] = processed_df

    return {
        "dataset_id": dataset_id,
        "final_rows": int(processed_df.shape[0]),
        "final_cols": int(processed_df.shape[1]),
        "stats": stats,
    }


@app.post("/api/v1/analyze/trends")
def analyze_trends(req: AnalyzeRequest) -> Dict[str, Any]:
    df = DATASETS.get(req.dataset_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    analyzer = TrendAnalyzer()
    results = analyzer.analyze_donation_trends(
        df,
        time_granularity=req.granularity,
        time_period_days=req.time_period_days,
    )

    return {
        "dataset_id": req.dataset_id,
        "trends": {k: v.dict() for k, v in results.items()},
    }


@app.post("/api/v1/analyze/forecast")
def analyze_forecast(req: ForecastRequest) -> Dict[str, Any]:
    df = DATASETS.get(req.dataset_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    forecaster = DemandForecaster()
    forecasts = forecaster.forecast_demand(
        df,
        forecast_horizon_days=req.forecast_horizon_days,
        model_types=req.model_types,
        granularity=req.granularity,
        target_variable=req.target_variable,
    )

    return {
        "dataset_id": req.dataset_id,
        "forecasts": {k: v.dict() for k, v in forecasts.items()},
        "comparison": forecaster.compare_forecasts(forecasts),
    }


@app.post("/api/v1/mine/patterns")
def mine_patterns(req: MiningRequest) -> Dict[str, Any]:
    df = DATASETS.get(req.dataset_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    engine = PatternMiningEngine()
    results = engine.discover_donor_patterns(df, pattern_types=req.pattern_types)

    return {"dataset_id": req.dataset_id, "patterns": results}


@app.post("/api/v1/mine/associations")
def mine_associations(req: AssociationRequest) -> Dict[str, Any]:
    df = DATASETS.get(req.dataset_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    analyzer = AssociationAnalyzer()
    results = analyzer.discover_association_rules(
        df,
        min_support=req.min_support,
        min_confidence=req.min_confidence,
        min_lift=req.min_lift,
        algorithm=req.algorithm,
    )

    return {"dataset_id": req.dataset_id, "associations": results}
