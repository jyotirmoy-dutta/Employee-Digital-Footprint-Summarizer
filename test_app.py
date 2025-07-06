#!/usr/bin/env python3
"""
Test script for Employee Digital Footprint Summarizer
This script tests the core functionality without requiring the GUI.
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_data_collectors():
    """Test the data collectors."""
    print("=== Testing Data Collectors ===")
    
    try:
        from data_collectors.logins import get_logins
        print("✓ Login collector imported successfully")
        
        logins = get_logins()
        print(f"✓ Collected {len(logins)} login events")
        
        if logins:
            print(f"  Sample login: {logins[0]}")
            
    except Exception as e:
        print(f"✗ Login collector failed: {e}")
    
    try:
        from data_collectors.file_shares import get_file_shares
        print("✓ File shares collector imported successfully")
        
        file_shares = get_file_shares()
        print(f"✓ Collected {len(file_shares)} file shares")
        
        if file_shares:
            print(f"  Sample file share: {file_shares[0]}")
            
    except Exception as e:
        print(f"✗ File shares collector failed: {e}")
    
    try:
        from data_collectors.app_usage import get_app_usage
        print("✓ App usage collector imported successfully")
        
        app_usage = get_app_usage()
        print(f"✓ Collected {len(app_usage)} app usage events")
        
        if app_usage:
            print(f"  Sample app: {app_usage[0]}")
            
    except Exception as e:
        print(f"✗ App usage collector failed: {e}")

def test_pdf_generator():
    """Test the PDF generator."""
    print("\n=== Testing PDF Generator ===")
    
    try:
        from report.pdf_generator import DigitalFootprintReport
        print("✓ PDF generator imported successfully")
        
        # Create sample data
        sample_logins = [
            {
                'timestamp': datetime.now(),
                'username': 'testuser',
                'host': 'localhost',
                'type': 'session',
                'source': 'test'
            }
        ]
        
        sample_files = [
            {
                'path': 'C:\\test\\file.txt',
                'timestamp': datetime.now(),
                'type': 'recent_file',
                'source': 'test'
            }
        ]
        
        sample_apps = [
            {
                'name': 'TestApp',
                'path': 'C:\\test\\app.exe',
                'start_time': datetime.now(),
                'type': 'running_process',
                'source': 'test'
            }
        ]
        
        # Generate test report
        output_path = "test_report.pdf"
        report_generator = DigitalFootprintReport(output_path)
        
        report_path = report_generator.generate_report(
            sample_logins, sample_files, sample_apps,
            user_info={'name': 'Test User'}
        )
        
        print(f"✓ Test report generated: {report_path}")
        
        # Check if file exists
        if os.path.exists(report_path):
            print(f"✓ Report file exists ({os.path.getsize(report_path)} bytes)")
        else:
            print("✗ Report file not found")
            
    except Exception as e:
        print(f"✗ PDF generator failed: {e}")

def test_utils():
    """Test utility functions."""
    print("\n=== Testing Utilities ===")
    
    try:
        from utils.helpers import get_system_info, format_timestamp, truncate_text
        print("✓ Utilities imported successfully")
        
        system_info = get_system_info()
        print(f"✓ System info collected: {system_info['platform']}")
        
        timestamp = format_timestamp(datetime.now())
        print(f"✓ Timestamp formatted: {timestamp}")
        
        truncated = truncate_text("This is a very long text that should be truncated", 20)
        print(f"✓ Text truncated: {truncated}")
        
    except Exception as e:
        print(f"✗ Utilities failed: {e}")

def main():
    """Run all tests."""
    print("Employee Digital Footprint Summarizer - Test Suite")
    print("=" * 50)
    
    test_data_collectors()
    test_pdf_generator()
    test_utils()
    
    print("\n=== Test Summary ===")
    print("If you see mostly ✓ marks above, the core functionality is working!")
    print("To run the full GUI application, install dependencies and run: python main.py")

if __name__ == "__main__":
    main() 