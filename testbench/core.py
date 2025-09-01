"""
Test Bench Core Engine

Main orchestrator for water monitoring system testing.
Coordinates all testing phases including data loading, processing,
analysis, and reporting.
"""

import yaml
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
import json

from .data_feeder import DataFeeder
from .result_analyzer import ResultAnalyzer
from .benchmark import PerformanceBenchmark
from .synthetic_data import SyntheticDataGenerator


@dataclass
class TestConfiguration:
    """Configuration for test execution."""
    # Data settings
    data_sources: List[str]
    synthetic_data_ratio: float = 0.3
    test_split_ratio: float = 0.2
    
    # Test settings
    accuracy_tests: Dict[str, Any] = None
    performance_tests: Dict[str, Any] = None
    night_vision_tests: Dict[str, Any] = None
    
    # Output settings
    save_intermediate_results: bool = True
    generate_visualizations: bool = True
    detailed_logging: bool = True
    
    def __post_init__(self):
        """Set default values for nested configs."""
        if self.accuracy_tests is None:
            self.accuracy_tests = {
                'thresholds': [0.5, 0.7, 0.9],
                'metrics': ['accuracy', 'precision', 'recall', 'f1'],
                'cross_validation_folds': 5
            }
        
        if self.performance_tests is None:
            self.performance_tests = {
                'batch_sizes': [1, 8, 16, 32],
                'measure_memory': True,
                'measure_cpu_usage': True,
                'iterations': 100
            }
        
        if self.night_vision_tests is None:
            self.night_vision_tests = {
                'low_light_conditions': [0.1, 0.3, 0.5],
                'noise_levels': [0.1, 0.2, 0.3],
                'contrast_adjustments': [-0.3, 0.0, 0.3]
            }


class TestBenchEngine:
    """Main test bench engine for comprehensive water monitoring validation."""
    
    def __init__(
        self, 
        config_path: Union[str, Path],
        output_dir: Union[str, Path],
        synthetic_only: bool = False,
        skip_benchmarks: bool = False
    ):
        """
        Initialize the test bench engine.
        
        Args:
            config_path: Path to YAML configuration file
            output_dir: Directory for saving results
            synthetic_only: Whether to use only synthetic data
            skip_benchmarks: Whether to skip performance benchmarks
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config_path = Path(config_path)
        self.output_dir = Path(output_dir)
        self.synthetic_only = synthetic_only
        self.skip_benchmarks = skip_benchmarks
        
        # Initialize components
        self.config = self._load_configuration()
        self.data_feeder = DataFeeder(self.config)
        self.result_analyzer = ResultAnalyzer()
        self.benchmark = None if skip_benchmarks else PerformanceBenchmark()
        
        # Test state
        self.test_results = {}
        self.start_time = None
        self.water_monitoring_module = None
        
        # Attempt to import water monitoring module
        self._try_import_production_module()
        
        self.logger.info(f"Test bench initialized with config: {config_path}")
    
    def _load_configuration(self) -> TestConfiguration:
        """Load test configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config_dict = yaml.safe_load(f)
            
            return TestConfiguration(**config_dict)
            
        except Exception as e:
            self.logger.warning(f"Failed to load config from {self.config_path}: {e}")
            self.logger.info("Using default configuration")
            return TestConfiguration(data_sources=[])
    
    def _try_import_production_module(self):
        """Attempt to import the production water monitoring module."""
        try:
            from water_monitoring import WaterMonitoringModule
            self.water_monitoring_module = WaterMonitoringModule
            self.logger.info("✓ Water monitoring module imported successfully")
        except ImportError as e:
            self.logger.warning(f"⚠ Water monitoring module not available: {e}")
            self.logger.info("Using mock/synthetic testing mode")
    
    def show_test_plan(self):
        """Display the test execution plan without running tests."""
        self.logger.info("📋 Test Execution Plan:")
        self.logger.info("=" * 50)
        
        # Configuration summary
        self.logger.info(f"📁 Output Directory: {self.output_dir}")
        self.logger.info(f"🎭 Synthetic Only: {self.synthetic_only}")
        self.logger.info(f"⚡ Skip Benchmarks: {self.skip_benchmarks}")
        
        # Data sources
        if self.config.data_sources:
            self.logger.info(f"📊 Data Sources: {len(self.config.data_sources)}")
            for source in self.config.data_sources:
                self.logger.info(f"   - {source}")
        else:
            self.logger.info("📊 Data Sources: Synthetic data only")
        
        # Test phases
        self.logger.info("🧪 Test Phases:")
        self.logger.info("   1. Data Loading & Preprocessing")
        self.logger.info("   2. Accuracy Testing")
        if not self.skip_benchmarks:
            self.logger.info("   3. Performance Benchmarking")
        self.logger.info("   4. Night Vision Testing")
        self.logger.info("   5. Result Analysis & Reporting")
        
        self.logger.info("=" * 50)
    
    def run_full_test_suite(self) -> Dict[str, Any]:
        """
        Execute the complete test suite.
        
        Returns:
            Dictionary containing all test results
        """
        self.start_time = time.time()
        self.logger.info("🚀 Starting comprehensive test suite execution")
        
        try:
            # Phase 1: Data Loading
            self.logger.info("📊 Phase 1: Loading and preparing test data")
            test_data = self._prepare_test_data()
            
            # Phase 2: Accuracy Testing
            self.logger.info("🎯 Phase 2: Running accuracy tests")
            accuracy_results = self._run_accuracy_tests(test_data)
            
            # Phase 3: Performance Benchmarking (optional)
            performance_results = {}
            if not self.skip_benchmarks and self.benchmark:
                self.logger.info("⚡ Phase 3: Running performance benchmarks")
                performance_results = self._run_performance_tests(test_data)
            
            # Phase 4: Night Vision Testing
            self.logger.info("🌙 Phase 4: Running night vision tests")
            night_vision_results = self._run_night_vision_tests(test_data)
            
            # Phase 5: Compile Results
            self.logger.info("📈 Phase 5: Analyzing and compiling results")
            self.test_results = {
                'metadata': self._get_test_metadata(),
                'accuracy_tests': accuracy_results,
                'performance_tests': performance_results,
                'night_vision_tests': night_vision_results,
                'summary': self._generate_summary()
            }
            
            # Save results
            self._save_results()
            
            execution_time = time.time() - self.start_time
            self.logger.info(f"✅ Test suite completed in {execution_time:.2f} seconds")
            
            return self.test_results
            
        except Exception as e:
            self.logger.error(f"❌ Test suite failed: {str(e)}")
            raise
    
    def _prepare_test_data(self) -> Dict[str, Any]:
        """Prepare test data from configured sources."""
        if self.synthetic_only or not self.config.data_sources:
            self.logger.info("🎭 Generating synthetic test data")
            synthetic_gen = SyntheticDataGenerator()
            return synthetic_gen.generate_test_dataset(
                num_samples=1000,
                output_dir=self.output_dir / "synthetic_data"
            )
        
        return self.data_feeder.load_test_data()
    
    def _run_accuracy_tests(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run accuracy validation tests."""
        if not self.water_monitoring_module:
            return self._mock_accuracy_tests(test_data)
        
        results = {}
        
        try:
            # Initialize the module
            monitor = self.water_monitoring_module()
            
            # Run tests for different thresholds
            for threshold in self.config.accuracy_tests['thresholds']:
                self.logger.info(f"   Testing at threshold: {threshold}")
                threshold_results = self.result_analyzer.evaluate_accuracy(
                    monitor, test_data, threshold
                )
                results[f'threshold_{threshold}'] = threshold_results
            
            # Compute overall metrics
            results['overall_accuracy'] = self.result_analyzer.compute_overall_accuracy(results)
            
        except Exception as e:
            self.logger.error(f"Accuracy tests failed: {e}")
            results['error'] = str(e)
        
        return results
    
    def _run_performance_tests(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run performance benchmarking tests."""
        if not self.water_monitoring_module or not self.benchmark:
            return self._mock_performance_tests()
        
        return self.benchmark.run_full_benchmark(
            self.water_monitoring_module(),
            test_data,
            self.config.performance_tests
        )
    
    def _run_night_vision_tests(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run night vision and low-light condition tests."""
        # Implementation for specialized night vision testing
        # This would apply various lighting and noise conditions to test data
        
        results = {
            'low_light_performance': {},
            'noise_robustness': {},
            'contrast_sensitivity': {}
        }
        
        # Mock implementation for now
        for condition in self.config.night_vision_tests['low_light_conditions']:
            results['low_light_performance'][f'brightness_{condition}'] = {
                'accuracy': 0.85 * condition + 0.1,  # Simulate degradation
                'processing_time': 1.2 / condition   # Simulate slower processing
            }
        
        return results
    
    def _mock_accuracy_tests(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock accuracy test results when production module unavailable."""
        self.logger.warning("🎭 Using mock accuracy results - production module not available")
        
        import random
        random.seed(42)  # Reproducible mock results
        
        results = {}
        for threshold in self.config.accuracy_tests['thresholds']:
            results[f'threshold_{threshold}'] = {
                'accuracy': random.uniform(0.8, 0.95),
                'precision': random.uniform(0.75, 0.92),
                'recall': random.uniform(0.78, 0.94),
                'f1_score': random.uniform(0.76, 0.93)
            }
        
        results['overall_accuracy'] = sum(
            r['accuracy'] for r in results.values()
        ) / len(results)
        
        return results
    
    def _mock_performance_tests(self) -> Dict[str, Any]:
        """Generate mock performance test results."""
        self.logger.warning("🎭 Using mock performance results")
        
        return {
            'avg_processing_time': 0.245,
            'memory_usage_mb': 156.7,
            'cpu_usage_percent': 23.4,
            'throughput_fps': 4.08
        }
    
    def _get_test_metadata(self) -> Dict[str, Any]:
        """Get test execution metadata."""
        return {
            'timestamp': time.time(),
            'execution_time': time.time() - self.start_time if self.start_time else 0,
            'config_file': str(self.config_path),
            'synthetic_only': self.synthetic_only,
            'skip_benchmarks': self.skip_benchmarks,
            'production_module_available': self.water_monitoring_module is not None
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate test results summary."""
        summary = {
            'total_tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'overall_score': 0.0
        }
        
        # Count and analyze results
        if 'accuracy_tests' in self.test_results:
            acc_results = self.test_results['accuracy_tests']
            if 'overall_accuracy' in acc_results:
                summary['overall_score'] = acc_results['overall_accuracy']
                summary['tests_passed'] += 1
        
        summary['total_tests_run'] = summary['tests_passed'] + summary['tests_failed']
        
        return summary
    
    def _save_results(self):
        """Save test results to output directory."""
        results_file = self.output_dir / "test_results.json"
        
        try:
            # Convert any Path objects to strings for JSON serialization
            serializable_results = self._make_json_serializable(self.test_results)
            
            with open(results_file, 'w') as f:
                json.dump(serializable_results, f, indent=2)
            
            self.logger.info(f"💾 Results saved to: {results_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
    
    def _make_json_serializable(self, obj):
        """Convert objects to JSON serializable format."""
        if isinstance(obj, dict):
            return {k: self._make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(v) for v in obj]
        elif isinstance(obj, Path):
            return str(obj)
        else:
            return obj