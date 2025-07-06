#!/usr/bin/env python3
"""
Command Line Interface for Employee Digital Footprint Summarizer
"""

import argparse
import sys
import os
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_collectors.logins import get_logins
from data_collectors.file_shares import get_file_shares
from data_collectors.app_usage import get_app_usage
from report.pdf_generator import DigitalFootprintReport
from utils.helpers import (get_system_info, create_output_directory, 
                          get_unique_filename, save_report_metadata,
                          filter_data_by_date_range)

def collect_data(collect_logins=True, collect_files=True, collect_apps=True):
    """Collect data based on user preferences."""
    data = {}
    
    if collect_logins:
        print("Collecting login data...")
        data['logins'] = get_logins()
        print(f"✓ Collected {len(data['logins'])} login events")
    
    if collect_files:
        print("Collecting file shares data...")
        data['file_shares'] = get_file_shares()
        print(f"✓ Collected {len(data['file_shares'])} file shares")
    
    if collect_apps:
        print("Collecting application usage data...")
        data['app_usage'] = get_app_usage()
        print(f"✓ Collected {len(data['app_usage'])} application events")
    
    return data

def generate_report(data, output_path, title, start_date=None, end_date=None):
    """Generate PDF report."""
    print(f"Generating report: {title}")
    
    # Filter data by date range if specified
    if start_date and end_date:
        print(f"Filtering data from {start_date} to {end_date}")
        filtered_data = {}
        for key, items in data.items():
            filtered_data[key] = filter_data_by_date_range(items, start_date, end_date)
        data = filtered_data
    
    # Create report
    report_generator = DigitalFootprintReport(output_path)
    
    user_info = {'name': get_system_info()['username']}
    date_range = {'start': start_date, 'end': end_date} if start_date and end_date else None
    
    report_path = report_generator.generate_report(
        data.get('logins', []),
        data.get('file_shares', []),
        data.get('app_usage', []),
        user_info=user_info,
        date_range=date_range
    )
    
    # Save metadata
    metadata = {
        'title': title,
        'generated_at': datetime.now().isoformat(),
        'data_counts': {
            'logins': len(data.get('logins', [])),
            'file_shares': len(data.get('file_shares', [])),
            'app_usage': len(data.get('app_usage', []))
        },
        'date_range': {
            'start': start_date.isoformat() if start_date else None,
            'end': end_date.isoformat() if end_date else None
        }
    }
    save_report_metadata(report_path, metadata)
    
    return report_path

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Employee Digital Footprint Summarizer - CLI Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate full report
  python cli.py --output report.pdf
  
  # Collect only login data
  python cli.py --logins-only --output login_report.pdf
  
  # Filter by date range
  python cli.py --start-date 2024-01-01 --end-date 2024-01-31 --output monthly_report.pdf
  
  # Custom title
  python cli.py --title "Q1 2024 Digital Footprint" --output q1_report.pdf
        """
    )
    
    # Data collection options
    parser.add_argument('--logins-only', action='store_true',
                       help='Collect only login data')
    parser.add_argument('--files-only', action='store_true',
                       help='Collect only file shares data')
    parser.add_argument('--apps-only', action='store_true',
                       help='Collect only application usage data')
    parser.add_argument('--no-logins', action='store_true',
                       help='Skip login data collection')
    parser.add_argument('--no-files', action='store_true',
                       help='Skip file shares data collection')
    parser.add_argument('--no-apps', action='store_true',
                       help='Skip application usage data collection')
    
    # Report options
    parser.add_argument('--output', '-o', default=None,
                       help='Output PDF file path')
    parser.add_argument('--title', '-t', default="Employee Digital Footprint Report",
                       help='Report title')
    parser.add_argument('--start-date', type=str,
                       help='Start date for filtering (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str,
                       help='End date for filtering (YYYY-MM-DD)')
    
    # System info
    parser.add_argument('--system-info', action='store_true',
                       help='Display system information and exit')
    
    args = parser.parse_args()
    
    # Display system info if requested
    if args.system_info:
        system_info = get_system_info()
        print("System Information:")
        for key, value in system_info.items():
            print(f"  {key}: {value}")
        return
    
    # Determine what to collect
    collect_logins = not args.no_logins and not args.files_only and not args.apps_only
    collect_files = not args.no_files and not args.logins_only and not args.apps_only
    collect_apps = not args.no_apps and not args.logins_only and not args.files_only
    
    if not any([collect_logins, collect_files, collect_apps]):
        print("Error: No data types selected for collection.")
        print("Use --logins-only, --files-only, --apps-only, or remove --no-* flags.")
        return 1
    
    # Parse dates if provided
    start_date = None
    end_date = None
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, '%Y-%m-%d').date()
        except ValueError:
            print(f"Error: Invalid start date format: {args.start_date}")
            print("Use YYYY-MM-DD format (e.g., 2024-01-01)")
            return 1
    
    if args.end_date:
        try:
            end_date = datetime.strptime(args.end_date, '%Y-%m-%d').date()
        except ValueError:
            print(f"Error: Invalid end date format: {args.end_date}")
            print("Use YYYY-MM-DD format (e.g., 2024-01-31)")
            return 1
    
    # Validate date range
    if start_date and end_date and start_date > end_date:
        print("Error: Start date must be before end date")
        return 1
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_dir = create_output_directory()
        filename = get_unique_filename("digital_footprint_report")
        output_path = os.path.join(output_dir, filename)
    
    print("Employee Digital Footprint Summarizer - CLI")
    print("=" * 50)
    
    # Collect data
    try:
        data = collect_data(collect_logins, collect_files, collect_apps)
        
        if not any(data.values()):
            print("Warning: No data collected. Check your system permissions.")
            return 1
        
        # Generate report
        report_path = generate_report(data, output_path, args.title, start_date, end_date)
        
        print(f"\n✓ Report generated successfully!")
        print(f"  File: {report_path}")
        print(f"  Size: {os.path.getsize(report_path)} bytes")
        
        # Summary
        total_items = sum(len(items) for items in data.values())
        print(f"\nSummary:")
        print(f"  Total data points: {total_items}")
        for key, items in data.items():
            print(f"  {key}: {len(items)} items")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 