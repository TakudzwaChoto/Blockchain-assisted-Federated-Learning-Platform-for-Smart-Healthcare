"""
Batch data processing engine for blood domain
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
import logging
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

from .data_cleaner import DataCleaner
from .data_transformer import DataTransformer
from .data_validator import DataValidator
from .import_handlers import ImportHandlerFactory
from ..models.donor import BatchDonationData
from ..models.validation import BatchValidationResult
from ..config import Config

class BatchDataProcessor:
    """High-performance batch data processing engine"""
    
    def __init__(self, max_workers: int = 4, batch_size: int = 10000):
        self.max_workers = max_workers
        self.batch_size = batch_size
        self.cleaner = DataCleaner()
        self.transformer = DataTransformer()
        self.validator = DataValidator()
        self.import_factory = ImportHandlerFactory()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Processing statistics
        self.processing_stats = {
            "total_batches_processed": 0,
            "total_records_processed": 0,
            "total_processing_time": 0,
            "average_processing_speed": 0
        }
    
    async def process_batch_file(self, file_path: str, file_format: str = None, 
                               processing_options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a single batch file end-to-end"""
        start_time = datetime.now()
        
        try:
            # Determine file format if not specified
            if file_format is None:
                file_format = Path(file_path).suffix.lower().replace(".", "")
            
            # Import data
            self.logger.info(f"Importing data from {file_path}")
            raw_data, import_stats = await self._import_data(file_path, file_format)
            
            # Process data in chunks if large
            if len(raw_data) > self.batch_size:
                processed_data, processing_stats = await self._process_large_dataset(raw_data, processing_options)
            else:
                processed_data, processing_stats = await self._process_dataset(raw_data, processing_options)
            
            # Calculate final statistics
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            
            result = {
                "success": True,
                "file_path": file_path,
                "file_format": file_format,
                "processing_time_seconds": total_time,
                "import_stats": import_stats,
                "processing_stats": processing_stats,
                "final_data_shape": processed_data.shape if processed_data is not None else (0, 0),
                "data_quality_score": processing_stats.get("data_quality_score", 0),
                "processed_at": end_time.isoformat()
            }
            
            # Update global statistics
            self._update_global_stats(result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing batch file {file_path}: {str(e)}")
            return {
                "success": False,
                "file_path": file_path,
                "error": str(e),
                "processed_at": datetime.now().isoformat()
            }
    
    async def process_multiple_files(self, file_paths: List[str], 
                                   processing_options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Process multiple files concurrently"""
        tasks = []
        
        for file_path in file_paths:
            task = self.process_batch_file(file_path, processing_options=processing_options)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "success": False,
                    "file_path": file_paths[i],
                    "error": str(result),
                    "processed_at": datetime.now().isoformat()
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _import_data(self, file_path: str, file_format: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Import data using appropriate handler"""
        handler = self.import_factory.get_handler(file_format)
        return await handler.import_data(file_path)
    
    async def _process_dataset(self, data: pd.DataFrame, 
                            processing_options: Dict[str, Any] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process a dataset with all cleaning, transformation, and validation steps"""
        if processing_options is None:
            processing_options = {
                "clean_data": True,
                "transform_data": True,
                "validate_data": True,
                "generate_reports": True
            }
        
        processing_stats = {
            "steps_completed": [],
            "records_at_each_step": {"original": len(data)},
            "validation_results": None,
            "data_quality_score": 0
        }
        
        current_data = data.copy()
        
        # Step 1: Data Cleaning
        if processing_options.get("clean_data", True):
            self.logger.info("Starting data cleaning...")
            cleaned_data, cleaning_stats = self.cleaner.clean_dataset(current_data)
            current_data = cleaned_data
            processing_stats["steps_completed"].append("data_cleaning")
            processing_stats["records_at_each_step"]["after_cleaning"] = len(current_data)
            processing_stats["cleaning_stats"] = cleaning_stats
        
        # Step 2: Data Transformation
        if processing_options.get("transform_data", True):
            self.logger.info("Starting data transformation...")
            transformed_data, transformation_stats = self.transformer.transform_dataset(current_data)
            current_data = transformed_data
            processing_stats["steps_completed"].append("data_transformation")
            processing_stats["records_at_each_step"]["after_transformation"] = len(current_data)
            processing_stats["transformation_stats"] = transformation_stats
        
        # Step 3: Data Validation
        if processing_options.get("validate_data", True):
            self.logger.info("Starting data validation...")
            batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            validation_result = self.validator.validate_batch(current_data, batch_id)
            processing_stats["steps_completed"].append("data_validation")
            processing_stats["validation_results"] = validation_result.dict()
            processing_stats["data_quality_score"] = self.validator.get_quality_metrics(validation_result.validation_results).get("overall_score", 0)
        
        # Step 4: Generate processing reports
        if processing_options.get("generate_reports", True):
            processing_stats["processing_report"] = self._generate_processing_report(processing_stats)
        
        return current_data, processing_stats
    
    async def _process_large_dataset(self, data: pd.DataFrame, 
                                   processing_options: Dict[str, Any] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process large dataset in chunks"""
        self.logger.info(f"Processing large dataset with {len(data)} records in chunks of {self.batch_size}")
        
        chunks = [data[i:i + self.batch_size] for i in range(0, len(data), self.batch_size)]
        processed_chunks = []
        chunk_stats = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all chunks for processing
            future_to_chunk = {
                executor.submit(self._process_chunk_sync, chunk, processing_options): i 
                for i, chunk in enumerate(chunks)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_chunk):
                chunk_idx = future_to_chunk[future]
                try:
                    processed_chunk, stats = future.result()
                    processed_chunks.append(processed_chunk)
                    chunk_stats.append(stats)
                except Exception as e:
                    self.logger.error(f"Error processing chunk {chunk_idx}: {str(e)}")
                    # Add original chunk if processing failed
                    processed_chunks.append(chunks[chunk_idx])
                    chunk_stats.append({"error": str(e)})
        
        # Combine all processed chunks
        final_data = pd.concat(processed_chunks, ignore_index=True)
        
        # Aggregate statistics
        aggregated_stats = self._aggregate_chunk_stats(chunk_stats)
        aggregated_stats["chunks_processed"] = len(chunks)
        aggregated_stats["chunk_size"] = self.batch_size
        
        return final_data, aggregated_stats
    
    def _process_chunk_sync(self, chunk: pd.DataFrame, 
                          processing_options: Dict[str, Any] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Synchronous chunk processing for ThreadPoolExecutor"""
        # This is a wrapper around the async processing method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self._process_dataset(chunk, processing_options))
        finally:
            loop.close()
    
    def _aggregate_chunk_stats(self, chunk_stats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate statistics from multiple chunks"""
        aggregated = {
            "steps_completed": [],
            "total_records_processed": 0,
            "total_records_removed": 0,
            "total_records_modified": 0,
            "average_quality_score": 0,
            "processing_errors": []
        }
        
        quality_scores = []
        
        for stats in chunk_stats:
            if "error" in stats:
                aggregated["processing_errors"].append(stats["error"])
                continue
            
            aggregated["total_records_processed"] += stats.get("records_at_each_step", {}).get("original", 0)
            
            if "cleaning_stats" in stats:
                aggregated["total_records_removed"] += stats["cleaning_stats"].get("records_removed", 0)
                aggregated["total_records_modified"] += stats["cleaning_stats"].get("records_modified", 0)
            
            if "data_quality_score" in stats:
                quality_scores.append(stats["data_quality_score"])
            
            # Collect unique steps
            for step in stats.get("steps_completed", []):
                if step not in aggregated["steps_completed"]:
                    aggregated["steps_completed"].append(step)
        
        if quality_scores:
            aggregated["average_quality_score"] = sum(quality_scores) / len(quality_scores)
        
        return aggregated
    
    def _generate_processing_report(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive processing report"""
        report = {
            "summary": {
                "total_steps": len(stats.get("steps_completed", [])),
                "processing_success": True,
                "data_quality_score": stats.get("data_quality_score", 0)
            },
            "data_flow": stats.get("records_at_each_step", {}),
            "quality_metrics": {
                "completeness": stats.get("data_quality_score", 0),
                "consistency": stats.get("validation_results", {}).get("summary_by_severity", {}),
                "accuracy": stats.get("validation_results", {}).get("valid_records", 0) / max(stats.get("validation_results", {}).get("total_records", 1), 1) * 100
            },
            "recommendations": self._generate_recommendations(stats)
        }
        
        return report
    
    def _generate_recommendations(self, stats: Dict[str, Any]) -> List[str]:
        """Generate processing recommendations based on statistics"""
        recommendations = []
        
        quality_score = stats.get("data_quality_score", 0)
        if quality_score < 70:
            recommendations.append("Data quality is below threshold. Consider additional cleaning steps.")
        
        validation_results = stats.get("validation_results", {})
        if validation_results.get("invalid_records", 0) > validation_results.get("total_records", 0) * 0.1:
            recommendations.append("High validation error rate detected. Review validation rules.")
        
        cleaning_stats = stats.get("cleaning_stats", {})
        if cleaning_stats.get("records_removed", 0) > cleaning_stats.get("original_records", 0) * 0.2:
            recommendations.append("Large number of records removed during cleaning. Review data source quality.")
        
        if not recommendations:
            recommendations.append("Data processing completed successfully with good quality metrics.")
        
        return recommendations
    
    def _update_global_stats(self, result: Dict[str, Any]) -> None:
        """Update global processing statistics"""
        if result.get("success", False):
            self.processing_stats["total_batches_processed"] += 1
            self.processing_stats["total_records_processed"] += result.get("final_data_shape", (0, 0))[0]
            self.processing_stats["total_processing_time"] += result.get("processing_time_seconds", 0)
            
            if self.processing_stats["total_processing_time"] > 0:
                self.processing_stats["average_processing_speed"] = (
                    self.processing_stats["total_records_processed"] / 
                    self.processing_stats["total_processing_time"]
                )
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get global processing statistics"""
        return self.processing_stats.copy()
    
    def export_processed_data(self, data: pd.DataFrame, output_path: str, 
                           format: str = "csv") -> Dict[str, Any]:
        """Export processed data to specified format"""
        try:
            if format.lower() == "csv":
                data.to_csv(output_path, index=False)
            elif format.lower() == "excel":
                data.to_excel(output_path, index=False)
            elif format.lower() == "json":
                data.to_json(output_path, orient="records", date_format="iso")
            elif format.lower() == "parquet":
                data.to_parquet(output_path, index=False)
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            return {
                "success": True,
                "output_path": output_path,
                "format": format,
                "records_exported": len(data),
                "file_size_mb": Path(output_path).stat().st_size / (1024 * 1024),
                "exported_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "exported_at": datetime.now().isoformat()
            }
