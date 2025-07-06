# Employee Digital Footprint Summarizer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/yourusername/footprintSummarizer)
[![PyPI](https://img.shields.io/badge/PyPI-Not%20Published-red.svg)](https://pypi.org/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://github.com/yourusername/footprintSummarizer)

> **A comprehensive, cross-platform tool for generating professional digital footprint reports from employee system activity.**

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## 🎯 Overview

The **Employee Digital Footprint Summarizer** is a professional-grade tool designed for IT administrators, security professionals, and compliance officers. It aggregates user digital activity—including logins, file shares, and application usage—into comprehensive PDF reports suitable for audits, compliance, and employee offboarding processes.

### Key Benefits

- **🔍 Comprehensive Data Collection**: Captures login events, file access patterns, and application usage
- **📊 Professional Reports**: Generates audit-ready PDF reports with executive summaries
- **🖥️ Cross-Platform**: Works on Windows, macOS, and Linux systems
- **⚡ Dual Interface**: Both GUI and command-line interfaces for maximum flexibility
- **🔒 Privacy-Focused**: Local data processing with no external dependencies
- **🛡️ Enterprise-Ready**: Designed for corporate environments and compliance requirements

## ✨ Features

### Core Functionality
- **Multi-Source Data Collection**: Aggregates data from system logs, registry, and process monitoring
- **Professional PDF Generation**: Creates comprehensive reports with proper formatting and metadata
- **Cross-Platform Compatibility**: Modular architecture supporting Windows, macOS, and Linux
- **Dual Interface Options**: Modern GUI for interactive use and CLI for automation
- **Real-Time Data Preview**: Live preview of collected data before report generation

### Data Sources
- **🔐 Login Events**: User sessions, authentication logs, and login history
- **📁 File Shares**: Recent files, network drives, and shared folder access
- **💻 Application Usage**: Running processes, installed applications, and resource usage
- **🖥️ System Information**: Platform details, hardware information, and user context

### Report Features
- **📈 Executive Summary**: High-level overview with key metrics and statistics
- **📋 Detailed Sections**: Comprehensive breakdown of each data type with timestamps
- **📅 Date Filtering**: Customizable date ranges for targeted analysis
- **🎨 Professional Formatting**: Clean, audit-ready PDF output using industry standards
- **📊 Metadata Export**: JSON metadata files for further analysis and integration

### Advanced Capabilities
- **⚡ Threaded Operations**: Non-blocking data collection with progress indicators
- **🔄 Error Handling**: Robust error handling with user-friendly messages
- **🔧 Extensible Architecture**: Easy to add new data sources and report formats
- **📱 Responsive Design**: Modern interface that adapts to different screen sizes
- **🔍 Data Validation**: Comprehensive input validation and data integrity checks

### CLI Usage
```bash
$ python cli.py --system-info
System Information:
  platform: Windows
  platform_version: 10.0.26100
  machine: AMD64
  processor: AMD64 Family 23 Model 24 Stepping 1, AuthenticAMD
  username: current_user
```

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **Administrative privileges** (for accessing system logs and registry)
- **Windows**: No additional requirements
- **macOS**: Requires system permissions for log access
- **Linux**: Requires appropriate user permissions

### Option 1: Direct Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/footprintSummarizer.git
cd footprintSummarizer

# Install dependencies
pip install -r requirements.txt

# Test the installation
python test_app.py
```

### Option 2: Development Installation

```bash
# Clone and install in development mode
git clone https://github.com/yourusername/footprintSummarizer.git
cd footprintSummarizer
pip install -e .

# Run tests
python test_app.py
```

### Option 3: Standalone Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed main.py

# Run the executable
./dist/main.exe  # Windows
./dist/main      # macOS/Linux
```

## ⚡ Quick Start

### 1. Test Core Functionality
```bash
python test_app.py
```

### 2. Launch GUI Application
```bash
python main.py
```

### 3. Use Command Line Interface
```bash
# Generate a full report
python cli.py --output employee_report.pdf

# Show available options
python cli.py --help
```

## 📖 Usage

### GUI Interface

The graphical interface provides an intuitive way to collect data and generate reports:

1. **Data Collection Tab**: Configure what data to collect and set date ranges
2. **Data Preview Tab**: Review collected data before generating reports
3. **Report Generation Tab**: Customize report options and generate PDFs

### Command Line Interface

The CLI is perfect for automation, scripting, and server environments:

#### Basic Usage

```bash
# Generate full report with default settings
python cli.py --output report.pdf

# Collect specific data types only
python cli.py --logins-only --output login_report.pdf
python cli.py --files-only --output files_report.pdf
python cli.py --apps-only --output apps_report.pdf

# Skip specific data types
python cli.py --no-apps --output no_apps_report.pdf
```

#### Advanced Usage

```bash
# Filter by date range
python cli.py --start-date 2024-01-01 --end-date 2024-01-31 --output monthly_report.pdf

# Custom report title
python cli.py --title "Q1 2024 Digital Footprint Analysis" --output q1_report.pdf

# System information only
python cli.py --system-info

# Combine multiple options
python cli.py --logins-only --start-date 2024-01-01 --title "Login Analysis" --output login_analysis.pdf
```

#### CLI Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `--output, -o` | Output PDF file path | `--output report.pdf` |
| `--title, -t` | Report title | `--title "Custom Report"` |
| `--start-date` | Start date (YYYY-MM-DD) | `--start-date 2024-01-01` |
| `--end-date` | End date (YYYY-MM-DD) | `--end-date 2024-01-31` |
| `--logins-only` | Collect only login data | `--logins-only` |
| `--files-only` | Collect only file shares | `--files-only` |
| `--apps-only` | Collect only app usage | `--apps-only` |
| `--no-logins` | Skip login collection | `--no-logins` |
| `--no-files` | Skip file shares | `--no-files` |
| `--no-apps` | Skip app usage | `--no-apps` |
| `--system-info` | Show system info only | `--system-info` |

## 🔧 API Reference

### Core Functions

#### Data Collection

```python
from data_collectors.logins import get_logins
from data_collectors.file_shares import get_file_shares
from data_collectors.app_usage import get_app_usage

# Collect login events
logins = get_logins()

# Collect file shares
file_shares = get_file_shares()

# Collect application usage
app_usage = get_app_usage()
```

#### Report Generation

```python
from report.pdf_generator import DigitalFootprintReport

# Create report generator
report_gen = DigitalFootprintReport("output.pdf")

# Generate report
report_path = report_gen.generate_report(
    logins=logins,
    file_shares=file_shares,
    app_usage=app_usage,
    user_info={'name': 'John Doe'},
    date_range={'start': start_date, 'end': end_date}
)
```

#### Utility Functions

```python
from utils.helpers import (
    get_system_info,
    format_timestamp,
    filter_data_by_date_range,
    create_output_directory
)

# Get system information
system_info = get_system_info()

# Format timestamps
formatted_time = format_timestamp(datetime.now())

# Filter data by date range
filtered_data = filter_data_by_date_range(data, start_date, end_date)
```

### Data Structures

#### Login Event
```python
{
    'timestamp': datetime,
    'username': str,
    'host': str,
    'type': str,  # 'session', 'login', 'current'
    'source': str  # 'psutil', 'event_log', etc.
}
```

#### File Share
```python
{
    'path': str,
    'timestamp': datetime,
    'type': str,  # 'recent_file', 'network_drive', 'mounted_share'
    'source': str  # 'recent_folder', 'drive_check', 'registry'
}
```

#### Application Usage
```python
{
    'name': str,
    'path': str,
    'pid': int,
    'start_time': datetime,
    'cpu_percent': float,
    'memory_percent': float,
    'type': str,  # 'running_process', 'installed_app'
    'source': str  # 'psutil', 'registry'
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FOOTPRINT_OUTPUT_DIR` | Default output directory | `./reports` |
| `FOOTPRINT_LOG_LEVEL` | Logging level | `INFO` |
| `FOOTPRINT_MAX_RECORDS` | Maximum records per report | `1000` |

### Configuration File

Create a `config.json` file in the project root:

```json
{
    "output_directory": "./reports",
    "max_records_per_report": 1000,
    "date_format": "%Y-%m-%d %H:%M:%S",
    "report_title": "Employee Digital Footprint Report",
    "include_metadata": true,
    "log_level": "INFO"
}
```

## 🔍 Troubleshooting

### Common Issues

#### Permission Errors
```bash
# Windows: Run as Administrator
# macOS: Grant Full Disk Access
# Linux: Use sudo or appropriate permissions
```

#### Missing Dependencies
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### GUI Not Starting
```bash
# Check PySide6 installation
pip install PySide6 --upgrade

# Try CLI version
python cli.py --help
```

#### No Data Collected
```bash
# Check system permissions
python cli.py --system-info

# Test individual collectors
python -c "from data_collectors.logins import get_logins; print(get_logins())"
```

### Debug Mode

Enable debug logging:

```bash
# Set environment variable
export FOOTPRINT_LOG_LEVEL=DEBUG

# Or use Python
python -c "import logging; logging.basicConfig(level=logging.DEBUG)" main.py
```

### Log Files

Logs are written to:
- **Windows**: `%TEMP%/footprint_summarizer.log`
- **macOS/Linux**: `/tmp/footprint_summarizer.log`

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/footprintSummarizer.git
cd footprintSummarizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python test_app.py
pytest tests/

# Run linting
flake8 .
black .
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all functions
- Include unit tests for new features

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Community

- **GitHub Discussions**: [Join the discussion](https://github.com/yourusername/footprintSummarizer/discussions)
- **Issues**: [Report bugs or request features](https://github.com/yourusername/footprintSummarizer/issues)
- **Wiki**: [Community documentation](https://github.com/yourusername/footprintSummarizer/wiki)

## 🙏 Acknowledgments

- **psutil**: Cross-platform system and process utilities
- **PySide6**: Qt for Python - GUI framework
- **ReportLab**: PDF generation library
- **matplotlib**: Plotting and visualization library

## 📊 Project Status

| Component | Status | Version |
|-----------|--------|---------|
| Windows Support | ✅ Complete | 1.0.0 |
| macOS Support | 🔄 In Progress | 0.5.0 |
| Linux Support | 🔄 In Progress | 0.5.0 |
| GUI Interface | ✅ Complete | 1.0.0 |
| CLI Interface | ✅ Complete | 1.0.0 |
| PDF Reports | ✅ Complete | 1.0.0 |
| Documentation | ✅ Complete | 1.0.0 |

## 🔮 Roadmap

### Version 1.1.0 (Q2 2024)
- [ ] macOS data collection implementation
- [ ] Linux data collection implementation
- [ ] Enhanced error handling and logging
- [ ] Performance optimizations

### Version 1.2.0 (Q3 2024)
- [ ] Cloud service integration (O365, Google Workspace)
- [ ] Advanced analytics and visualizations
- [ ] Email integration for report distribution
- [ ] API for third-party integrations

### Version 2.0.0 (Q4 2024)
- [ ] Web-based interface
- [ ] Multi-user support
- [ ] Database backend for historical data
- [ ] Advanced reporting templates

---

**Made with ❤️ for the IT community**

*If you find this project useful, please consider giving it a ⭐ on GitHub!* 
