# Water Monitoring Test Bench

[![Tests](https://github.com/thamam/water_monitoring_tb/actions/workflows/test.yml/badge.svg)](https://github.com/thamam/water_monitoring_tb/actions/workflows/test.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Comprehensive test bench for validating the production water monitoring module. This repository provides an isolated testing environment to thoroughly evaluate the water flow detection system with real data and synthetic scenarios.

## 🎯 Overview

This test bench:
- **Imports and validates** the production water monitoring module
- **Feeds diverse datasets** (real facility images, synthetic data, edge cases)
- **Analyzes results** with comprehensive metrics and visualizations
- **Benchmarks performance** against production requirements
- **Generates reports** for production readiness assessment

## 📊 Key Features

### **Comprehensive Testing**
- ✅ **Real facility data** from 4 treatment plants
- ✅ **Synthetic test scenarios** for edge cases
- ✅ **Performance benchmarking** (<10ms target validation)
- ✅ **Accuracy validation** (99.36% target verification)
- ✅ **Night vision testing** (low-light scenario validation)
- ✅ **Thread safety testing** (concurrent processing validation)

### **Data Management**
- 📁 **Multiple data sources** (CSV, JSON, image directories)
- 🔄 **Batch processing** capabilities
- 📈 **Real-time streaming** simulation
- 🎨 **Synthetic data generation** for comprehensive coverage

### **Analysis & Reporting**
- 📊 **Performance dashboards** with real-time metrics
- 📈 **Accuracy analysis** with confusion matrices
- ⏱️ **Timing benchmarks** with statistical analysis
- 🎯 **Production readiness reports** with recommendations

## 🚀 Quick Start

### Installation

```bash
# Clone the test bench
git clone https://github.com/thamam/water_monitoring_tb.git
cd water_monitoring_tb

# Install dependencies
pip install -r requirements.txt

# Install the production module (adjust path as needed)
# Option 1: From local package
pip install /path/to/water_monitoring_package

# Option 2: From wheel file
pip install water_monitoring-2.1.0-py3-none-any.whl

# Option 3: Development mode (if you have the source)
pip install -e /path/to/water_monitoring_package
```

### Basic Usage

```bash
# Run comprehensive validation
python run_test_bench.py

# Run specific test categories
python run_test_bench.py --accuracy-only
python run_test_bench.py --performance-only
python run_test_bench.py --night-vision-only

# Run with custom data
python run_test_bench.py --data-dir /path/to/your/images

# Generate detailed reports
python run_test_bench.py --report --html
```

## 📁 Repository Structure

```
water_monitoring_tb/
├── testbench/                   # Core test bench modules
│   ├── __init__.py
│   ├── core.py                  # Main test bench engine
│   ├── data_feeder.py          # Data loading and management
│   ├── result_analyzer.py      # Result analysis and metrics
│   ├── benchmark.py            # Performance benchmarking
│   ├── report_generator.py     # Report generation
│   └── synthetic_data.py       # Synthetic test data generation
├── data/                        # Test datasets
│   ├── sample_images/          # Sample test images
│   ├── ground_truth/           # Ground truth annotations
│   ├── synthetic/              # Generated test scenarios
│   └── edge_cases/             # Edge case test data
├── configs/                     # Test configurations
│   ├── accuracy_test.yaml      # Accuracy validation config
│   ├── performance_test.yaml   # Performance benchmark config
│   ├── night_vision_test.yaml  # Low-light testing config
│   └── comprehensive.yaml      # Full test suite config
├── reports/                     # Generated test reports
│   ├── templates/              # Report templates
│   └── outputs/                # Generated reports
├── scripts/                     # Utility scripts
│   ├── download_test_data.py   # Download standard test datasets
│   ├── generate_synthetic.py   # Create synthetic test data
│   └── benchmark_comparison.py # Compare with baseline results
├── tests/                       # Test bench validation tests
│   └── test_testbench.py       # Tests for the test bench itself
├── .github/                     # GitHub Actions CI/CD
│   └── workflows/
│       ├── test.yml            # Continuous testing
│       └── benchmark.yml       # Performance monitoring
├── requirements.txt             # Dependencies
├── Dockerfile                   # Containerized testing
├── docker-compose.yml          # Multi-service testing
└── run_test_bench.py           # Main entry point
```

## 🧪 Test Categories

### **1. Accuracy Validation**
Validates the 99.36% accuracy claim using:
- Real facility images with ground truth labels
- Cross-validation across different lighting conditions
- Site-specific accuracy analysis
- Confusion matrix generation

### **2. Performance Benchmarking**
Validates performance requirements:
- Inference time <10ms validation
- Memory usage monitoring
- Throughput testing (images/second)
- GPU vs CPU performance comparison

### **3. Night Vision Testing**
Validates low-light enhancement:
- 92.5% accuracy in low-light conditions
- Enhancement effectiveness analysis
- Processing time impact assessment
- Before/after enhancement comparisons

### **4. Edge Case Testing**
Tests robustness with:
- Corrupted/malformed images
- Extreme lighting conditions
- Unusual image sizes and formats
- Network/hardware failure scenarios

### **5. Integration Testing**
Tests production scenarios:
- Concurrent processing capabilities
- Long-running stability tests
- Resource leak detection
- Error recovery validation

## 📊 Example Results

### Quick Validation
```bash
$ python run_test_bench.py --quick

🌊 Water Monitoring Test Bench v1.0
=====================================

✅ Module Import: SUCCESS (water_monitoring v2.1.0)
✅ Model Loading: SUCCESS (best_model.pth, 130MB)
✅ Device Detection: SUCCESS (cuda:0)
✅ Basic Inference: SUCCESS (8.3ms avg)

📊 Quick Accuracy Test (100 samples):
   - Overall Accuracy: 99.0%
   - Precision: 98.5%
   - Recall: 99.5%
   - F1 Score: 99.0%

⚡ Performance Benchmark:
   - Average Inference: 8.3ms ✅ (target: <10ms)
   - Throughput: 120.5 images/sec
   - Memory Usage: 1.8GB GPU, 0.9GB RAM ✅

🌙 Night Vision Test (50 low-light samples):
   - Low-light Accuracy: 92.8% ✅ (target: >92.5%)
   - Enhancement Applied: 94% of samples
   - Processing Overhead: +15.2ms avg

🎯 OVERALL: PRODUCTION READY ✅
```

### Comprehensive Report
```bash
$ python run_test_bench.py --comprehensive --report

# Generates detailed HTML report with:
# - Interactive accuracy charts
# - Performance timing histograms  
# - Night vision before/after examples
# - Confusion matrices
# - Resource usage graphs
# - Production readiness checklist
```

## 🐳 Docker Usage

```bash
# Build test bench image
docker build -t water-monitoring-tb .

# Run comprehensive tests
docker run -v $(pwd)/reports:/app/reports water-monitoring-tb

# Run with custom data
docker run -v /path/to/data:/app/custom_data -v $(pwd)/reports:/app/reports \
  water-monitoring-tb --data-dir /app/custom_data
```

## ⚙️ Configuration

Customize tests via YAML configuration files:

```yaml
# configs/custom_test.yaml
test_config:
  name: "Custom Accuracy Test"
  description: "Validate accuracy with custom dataset"
  
data:
  source: "/path/to/images"
  ground_truth: "/path/to/labels.csv"
  sample_size: 1000
  
validation:
  accuracy_threshold: 0.99
  performance_threshold_ms: 10
  memory_limit_gb: 2
  
reporting:
  generate_html: true
  include_visualizations: true
  save_failed_cases: true
```

## 🔍 Troubleshooting

### Common Issues

**Module Import Failures:**
```bash
# Verify production module installation
python -c "import water_monitoring; print(water_monitoring.__version__)"

# Check module path
python -c "import water_monitoring; print(water_monitoring.__file__)"
```

**Performance Issues:**
```bash
# Check GPU availability
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Monitor system resources
python run_test_bench.py --monitor-resources
```

**Data Loading Issues:**
```bash
# Validate data format
python scripts/validate_data.py --data-dir /path/to/data

# Download standard test data
python scripts/download_test_data.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-test`
3. Commit changes: `git commit -am 'Add new test scenario'`
4. Push to branch: `git push origin feature/new-test`
5. Submit a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [Water Monitoring Package](https://github.com/your-org/water_monitoring_package) - The production module being tested
- [Water Treatment Analytics](https://github.com/your-org/water_treatment_analytics) - Analysis and reporting tools

---

**Test Bench Version:** 1.0  
**Compatible with:** water-monitoring v2.1.0+  
**Python:** 3.8+  
**Last Updated:** September 2024