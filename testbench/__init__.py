"""
Water Monitoring Test Bench Package

A comprehensive testing framework for validating water monitoring systems.
Provides accuracy testing, performance benchmarking, synthetic data generation,
and detailed reporting capabilities.

Main Components:
- TestBenchEngine: Core testing orchestrator
- DataFeeder: Handles data loading and preprocessing
- ResultAnalyzer: Analyzes test results and computes metrics
- Benchmark: Performance and memory profiling
- ReportGenerator: Creates comprehensive HTML reports
- SyntheticDataGenerator: Generates realistic test data
"""

__version__ = "1.0.0"
__author__ = "Water Monitoring Team"
__description__ = "Comprehensive test bench for water monitoring systems"

# Core imports for easy access
from .core import TestBenchEngine
from .data_feeder import DataFeeder
from .result_analyzer import ResultAnalyzer
from .benchmark import PerformanceBenchmark
from .report_generator import ReportGenerator
from .synthetic_data import SyntheticDataGenerator

__all__ = [
    "TestBenchEngine",
    "DataFeeder", 
    "ResultAnalyzer",
    "PerformanceBenchmark",
    "ReportGenerator",
    "SyntheticDataGenerator"
]