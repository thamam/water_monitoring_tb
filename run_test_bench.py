#!/usr/bin/env python3
"""
Water Monitoring Test Bench - Main Entry Point

A comprehensive testing framework for validating water monitoring modules.
Supports accuracy testing, performance benchmarking, and synthetic data generation.

Usage:
    python run_test_bench.py --config configs/comprehensive.yaml
    python run_test_bench.py --config configs/quick_test.yaml --verbose
    python run_test_bench.py --synthetic-only --output results/
"""

import argparse
import sys
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Add testbench to path
sys.path.insert(0, str(Path(__file__).parent))

from testbench.core import TestBenchEngine
from testbench.report_generator import ReportGenerator
from testbench.synthetic_data import SyntheticDataGenerator


def setup_logging(verbose: bool = False, log_file: Optional[str] = None) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=handlers
    )


def validate_environment() -> Dict[str, Any]:
    """Validate the testing environment and return status."""
    status = {
        'water_monitoring_available': False,
        'gpu_available': False,
        'dependencies_ok': True,
        'errors': []
    }
    
    # Check for water monitoring module
    try:
        from water_monitoring import WaterMonitoringModule
        status['water_monitoring_available'] = True
        logging.info("✓ Water monitoring module found")
    except ImportError as e:
        status['errors'].append(f"Water monitoring module not found: {e}")
        logging.warning("⚠ Water monitoring module not available - will use mock/synthetic mode")
    
    # Check for GPU availability
    try:
        import torch
        if torch.cuda.is_available():
            status['gpu_available'] = True
            logging.info(f"✓ GPU available: {torch.cuda.get_device_name()}")
        else:
            logging.info("ℹ GPU not available - using CPU mode")
    except ImportError:
        logging.warning("⚠ PyTorch not available")
    
    # Check critical dependencies
    critical_deps = ['numpy', 'pandas', 'opencv-python', 'PIL', 'sklearn']
    for dep in critical_deps:
        try:
            __import__(dep.replace('-', '_'))
        except ImportError:
            status['dependencies_ok'] = False
            status['errors'].append(f"Critical dependency missing: {dep}")
    
    return status


def main():
    """Main entry point for the water monitoring test bench."""
    parser = argparse.ArgumentParser(
        description="Water Monitoring Test Bench - Comprehensive validation framework"
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        default="configs/comprehensive.yaml",
        help="Path to test configuration file"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="results/",
        help="Output directory for test results"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--log-file",
        type=str,
        help="Path to log file (optional)"
    )
    
    parser.add_argument(
        "--synthetic-only",
        action="store_true",
        help="Run tests using only synthetic data"
    )
    
    parser.add_argument(
        "--skip-benchmarks",
        action="store_true",
        help="Skip performance benchmarking tests"
    )
    
    parser.add_argument(
        "--generate-report-only",
        type=str,
        help="Generate report from existing results directory"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be tested without actually running"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose, args.log_file)
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("🌊 Water Monitoring Test Bench Starting")
    logger.info("=" * 60)
    
    try:
        # Validate environment
        env_status = validate_environment()
        if not env_status['dependencies_ok']:
            logger.error("❌ Critical dependencies missing:")
            for error in env_status['errors']:
                logger.error(f"   {error}")
            return 1
        
        # Create output directory
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Handle report-only mode
        if args.generate_report_only:
            logger.info(f"📊 Generating report from: {args.generate_report_only}")
            report_gen = ReportGenerator()
            report_path = report_gen.generate_from_results(
                Path(args.generate_report_only),
                output_dir / "report.html"
            )
            logger.info(f"✅ Report generated: {report_path}")
            return 0
        
        # Initialize test bench engine
        engine = TestBenchEngine(
            config_path=args.config,
            output_dir=output_dir,
            synthetic_only=args.synthetic_only or not env_status['water_monitoring_available'],
            skip_benchmarks=args.skip_benchmarks
        )
        
        # Dry run mode
        if args.dry_run:
            logger.info("🔍 Dry run mode - showing test plan:")
            engine.show_test_plan()
            return 0
        
        # Generate synthetic data if needed
        if args.synthetic_only or not env_status['water_monitoring_available']:
            logger.info("🎭 Generating synthetic test data...")
            synthetic_gen = SyntheticDataGenerator()
            synthetic_gen.generate_test_suite(output_dir / "synthetic_data")
        
        # Run the test suite
        logger.info("🚀 Starting test execution...")
        results = engine.run_full_test_suite()
        
        # Generate comprehensive report
        logger.info("📊 Generating test report...")
        report_gen = ReportGenerator()
        report_path = report_gen.generate_comprehensive_report(
            results, 
            output_dir / "test_report.html"
        )
        
        # Summary
        logger.info("=" * 60)
        logger.info("🏁 Test Bench Completed Successfully")
        logger.info(f"📁 Results saved to: {output_dir}")
        logger.info(f"📊 Report available at: {report_path}")
        logger.info("=" * 60)
        
        # Print quick summary
        if 'accuracy_tests' in results:
            acc = results['accuracy_tests'].get('overall_accuracy', 0)
            logger.info(f"🎯 Overall Accuracy: {acc:.2%}")
        
        if 'performance_tests' in results and not args.skip_benchmarks:
            perf = results['performance_tests']
            logger.info(f"⚡ Avg Processing Time: {perf.get('avg_processing_time', 0):.3f}s")
        
        return 0
        
    except KeyboardInterrupt:
        logger.warning("⚠ Test bench interrupted by user")
        return 130
        
    except Exception as e:
        logger.error(f"❌ Test bench failed with error: {str(e)}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    exit(main())