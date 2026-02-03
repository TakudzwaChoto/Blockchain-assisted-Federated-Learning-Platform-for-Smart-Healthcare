"""
Data import handlers for various file formats and sources
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import json
import sqlite3
import asyncio
import aiohttp
from sqlalchemy import create_engine, text
import logging

class BaseImportHandler:
    """Base class for all import handlers"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = []
    
    async def import_data(self, source: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Import data from source"""
        raise NotImplementedError("Subclasses must implement import_data method")
    
    def validate_source(self, source: str) -> bool:
        """Validate if source is accessible and valid"""
        raise NotImplementedError("Subclasses must implement validate_source method")
    
    def get_import_stats(self, data: pd.DataFrame, source: str) -> Dict[str, Any]:
        """Generate import statistics"""
        return {
            "source": source,
            "records_imported": len(data),
            "columns_imported": len(data.columns),
            "data_types": data.dtypes.to_dict(),
            "memory_usage_mb": data.memory_usage(deep=True).sum() / (1024 * 1024),
            "import_timestamp": datetime.now().isoformat()
        }

class CSVImporter(BaseImportHandler):
    """CSV file import handler"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ["csv", "tsv"]
    
    async def import_data(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Import data from CSV file"""
        try:
            # Default CSV parameters
            csv_params = {
                "encoding": "utf-8",
                "delimiter": ",",
                "header": 0,
                "na_values": ["", "NULL", "null", "N/A", "n/a", "None", "none"],
                "low_memory": False,
                "dtype": str  # Read all as string first, then convert types
            }
            
            # Override with user parameters
            csv_params.update(kwargs)
            
            # Read CSV file
            data = pd.read_csv(file_path, **csv_params)
            
            # Automatic type inference
            data = self._auto_infer_types(data)
            
            # Generate statistics
            stats = self.get_import_stats(data, file_path)
            stats["file_size_mb"] = Path(file_path).stat().st_size / (1024 * 1024)
            stats["csv_params"] = csv_params
            
            return data, stats
            
        except Exception as e:
            self.logger.error(f"Error importing CSV file {file_path}: {str(e)}")
            raise
    
    def validate_source(self, file_path: str) -> bool:
        """Validate CSV file"""
        try:
            path = Path(file_path)
            return path.exists() and path.is_file() and path.suffix.lower() in [".csv", ".tsv"]
        except:
            return False
    
    def _auto_infer_types(self, data: pd.DataFrame) -> pd.DataFrame:
        """Automatically infer and convert data types"""
        for column in data.columns:
            # Try to convert to datetime
            if any(keyword in column.lower() for keyword in ["date", "time", "created", "updated"]):
                data[column] = pd.to_datetime(data[column], errors='coerce')
                continue
            
            # Try to convert to numeric
            try:
                numeric_data = pd.to_numeric(data[column], errors='coerce')
                if not numeric_data.isna().all():
                    data[column] = numeric_data
                    continue
            except:
                pass
            
            # Keep as string if other conversions fail
            data[column] = data[column].astype(str)
        
        return data

class ExcelImporter(BaseImportHandler):
    """Excel file import handler"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ["xlsx", "xls", "xlsm"]
    
    async def import_data(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Import data from Excel file"""
        try:
            # Default Excel parameters
            excel_params = {
                "sheet_name": 0,  # First sheet
                "header": 0,
                "na_values": ["", "NULL", "null", "N/A", "n/a", "None", "none"],
                "dtype": str
            }
            
            # Override with user parameters
            excel_params.update(kwargs)
            
            # Read Excel file
            data = pd.read_excel(file_path, **excel_params)
            
            # Automatic type inference
            data = self._auto_infer_types(data)
            
            # Generate statistics
            stats = self.get_import_stats(data, file_path)
            stats["file_size_mb"] = Path(file_path).stat().st_size / (1024 * 1024)
            stats["sheet_name"] = excel_params.get("sheet_name", 0)
            
            return data, stats
            
        except Exception as e:
            self.logger.error(f"Error importing Excel file {file_path}: {str(e)}")
            raise
    
    def validate_source(self, file_path: str) -> bool:
        """Validate Excel file"""
        try:
            path = Path(file_path)
            return path.exists() and path.is_file() and path.suffix.lower() in [".xlsx", ".xls", ".xlsm"]
        except:
            return False
    
    def _auto_infer_types(self, data: pd.DataFrame) -> pd.DataFrame:
        """Same auto-inference logic as CSV"""
        csv_importer = CSVImporter()
        return csv_importer._auto_infer_types(data)

class JSONImporter(BaseImportHandler):
    """JSON file import handler"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ["json", "jsonl", "ndjson"]
    
    async def import_data(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Import data from JSON file"""
        try:
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == ".jsonl" or file_extension == ".ndjson":
                # Handle JSON Lines format
                data = self._read_json_lines(file_path)
            else:
                # Handle regular JSON
                json_params = {
                    "orient": "records",
                    "lines": False,
                    "encoding": "utf-8"
                }
                json_params.update(kwargs)
                
                data = pd.read_json(file_path, **json_params)
            
            # Automatic type inference
            data = self._auto_infer_types(data)
            
            # Generate statistics
            stats = self.get_import_stats(data, file_path)
            stats["file_size_mb"] = Path(file_path).stat().st_size / (1024 * 1024)
            stats["json_format"] = "lines" if file_extension in [".jsonl", ".ndjson"] else "regular"
            
            return data, stats
            
        except Exception as e:
            self.logger.error(f"Error importing JSON file {file_path}: {str(e)}")
            raise
    
    def validate_source(self, file_path: str) -> bool:
        """Validate JSON file"""
        try:
            path = Path(file_path)
            return path.exists() and path.is_file() and path.suffix.lower() in [".json", ".jsonl", ".ndjson"]
        except:
            return False
    
    def _read_json_lines(self, file_path: str) -> pd.DataFrame:
        """Read JSON Lines format"""
        records = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        record = json.loads(line)
                        records.append(record)
                    except json.JSONDecodeError:
                        continue
        
        return pd.DataFrame(records)
    
    def _auto_infer_types(self, data: pd.DataFrame) -> pd.DataFrame:
        """Same auto-inference logic as CSV"""
        csv_importer = CSVImporter()
        return csv_importer._auto_infer_types(data)

class SQLImporter(BaseImportHandler):
    """SQL database import handler"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ["sql", "database", "db"]
    
    async def import_data(self, connection_string: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Import data from SQL database"""
        try:
            # Default SQL parameters
            sql_params = {
                "query": kwargs.get("query", "SELECT * FROM donors LIMIT 1000000"),
                "chunksize": None
            }
            
            # Create database engine
            engine = create_engine(connection_string)
            
            # Execute query
            data = pd.read_sql(sql_params["query"], engine, chunksize=sql_params["chunksize"])
            
            # If chunksize is specified, combine chunks
            if sql_params["chunksize"]:
                data = pd.concat(data, ignore_index=True)
            
            # Generate statistics
            stats = self.get_import_stats(data, connection_string)
            stats["query"] = sql_params["query"]
            stats["database_type"] = self._get_database_type(connection_string)
            
            return data, stats
            
        except Exception as e:
            self.logger.error(f"Error importing from SQL database: {str(e)}")
            raise
    
    def validate_source(self, connection_string: str) -> bool:
        """Validate database connection"""
        try:
            engine = create_engine(connection_string)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except:
            return False
    
    def _get_database_type(self, connection_string: str) -> str:
        """Extract database type from connection string"""
        connection_string_lower = connection_string.lower()
        if "postgresql" in connection_string_lower:
            return "PostgreSQL"
        elif "mysql" in connection_string_lower:
            return "MySQL"
        elif "sqlite" in connection_string_lower:
            return "SQLite"
        elif "sqlserver" in connection_string_lower or "mssql" in connection_string_lower:
            return "SQL Server"
        else:
            return "Unknown"
    
    def _auto_infer_types(self, data: pd.DataFrame) -> pd.DataFrame:
        """SQL already provides proper types, but we can still do additional inference"""
        csv_importer = CSVImporter()
        return csv_importer._auto_infer_types(data)

class APIImporter(BaseImportHandler):
    """API endpoint import handler"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ["api", "rest", "endpoint"]
    
    async def import_data(self, api_url: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Import data from REST API"""
        try:
            # Default API parameters
            api_params = {
                "method": "GET",
                "headers": {"Content-Type": "application/json"},
                "params": {},
                "timeout": 30,
                "auth": None
            }
            
            # Override with user parameters
            api_params.update(kwargs)
            
            # Make API request
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    api_params["method"],
                    api_url,
                    headers=api_params["headers"],
                    params=api_params["params"],
                    timeout=aiohttp.ClientTimeout(total=api_params["timeout"]),
                    auth=api_params["auth"]
                ) as response:
                    if response.status != 200:
                        raise Exception(f"API request failed with status {response.status}")
                    
                    data_json = await response.json()
            
            # Convert to DataFrame
            if isinstance(data_json, list):
                data = pd.DataFrame(data_json)
            elif isinstance(data_json, dict):
                # Handle paginated responses or nested structures
                if "data" in data_json:
                    data = pd.DataFrame(data_json["data"])
                elif "results" in data_json:
                    data = pd.DataFrame(data_json["results"])
                else:
                    data = pd.DataFrame([data_json])
            else:
                raise ValueError("Unsupported API response format")
            
            # Automatic type inference
            data = self._auto_infer_types(data)
            
            # Generate statistics
            stats = self.get_import_stats(data, api_url)
            stats["api_url"] = api_url
            stats["response_status"] = response.status
            stats["response_size_mb"] = len(str(data_json)) / (1024 * 1024)
            
            return data, stats
            
        except Exception as e:
            self.logger.error(f"Error importing from API {api_url}: {str(e)}")
            raise
    
    def validate_source(self, api_url: str) -> bool:
        """Validate API endpoint accessibility"""
        try:
            import urllib.request
            req = urllib.request.Request(api_url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                status = getattr(resp, "status", 200)
                return int(status) < 500
        except Exception:
            return False
    
    def _auto_infer_types(self, data: pd.DataFrame) -> pd.DataFrame:
        """Same auto-inference logic as CSV"""
        csv_importer = CSVImporter()
        return csv_importer._auto_infer_types(data)

class ImportHandlerFactory:
    """Factory for creating appropriate import handlers"""
    
    def __init__(self):
        self.handlers = {
            "csv": CSVImporter,
            "tsv": CSVImporter,
            "xlsx": ExcelImporter,
            "xls": ExcelImporter,
            "xlsm": ExcelImporter,
            "json": JSONImporter,
            "jsonl": JSONImporter,
            "ndjson": JSONImporter,
            "sql": SQLImporter,
            "database": SQLImporter,
            "db": SQLImporter,
            "api": APIImporter,
            "rest": APIImporter,
            "endpoint": APIImporter
        }
    
    def get_handler(self, format_type: str) -> BaseImportHandler:
        """Get appropriate handler for format"""
        format_type = format_type.lower()
        
        if format_type in self.handlers:
            return self.handlers[format_type]()
        else:
            raise ValueError(f"Unsupported format: {format_type}. Supported formats: {list(self.handlers.keys())}")
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported formats"""
        return list(self.handlers.keys())
    
    def register_handler(self, format_type: str, handler_class: type) -> None:
        """Register a custom handler"""
        if not issubclass(handler_class, BaseImportHandler):
            raise ValueError("Handler must inherit from BaseImportHandler")
        
        self.handlers[format_type.lower()] = handler_class
