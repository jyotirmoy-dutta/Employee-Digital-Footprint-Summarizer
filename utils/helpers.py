import os
import platform
from datetime import datetime, timedelta
import json

def get_system_info():
    """Get basic system information."""
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'hostname': platform.node(),
        'username': os.getenv('USERNAME') or os.getenv('USER', 'Unknown')
    }

def format_timestamp(timestamp):
    """Format timestamp for display."""
    if isinstance(timestamp, datetime):
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(timestamp, (int, float)):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return str(timestamp)

def truncate_text(text, max_length=50):
    """Truncate text to specified length with ellipsis."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def validate_date_range(start_date, end_date):
    """Validate date range."""
    if not start_date or not end_date:
        return False, "Both start and end dates are required"
    
    if start_date > end_date:
        return False, "Start date must be before end date"
    
    if end_date > datetime.now():
        return False, "End date cannot be in the future"
    
    return True, "Valid date range"

def create_output_directory():
    """Create output directory for reports."""
    output_dir = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def get_unique_filename(base_name, extension=".pdf"):
    """Generate unique filename to avoid overwrites."""
    counter = 1
    filename = f"{base_name}{extension}"
    
    while os.path.exists(filename):
        filename = f"{base_name}_{counter}{extension}"
        counter += 1
    
    return filename

def save_report_metadata(report_path, metadata):
    """Save report metadata to JSON file."""
    metadata_path = report_path.replace('.pdf', '_metadata.json')
    try:
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving metadata: {e}")
        return False

def load_report_metadata(report_path):
    """Load report metadata from JSON file."""
    metadata_path = report_path.replace('.pdf', '_metadata.json')
    try:
        with open(metadata_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return None

def filter_data_by_date_range(data, start_date, end_date, date_field='timestamp'):
    """Filter data by date range."""
    if not start_date or not end_date:
        return data
    
    filtered_data = []
    for item in data:
        item_date = item.get(date_field)
        if item_date:
            if isinstance(item_date, str):
                try:
                    item_date = datetime.fromisoformat(item_date.replace('Z', '+00:00'))
                except:
                    continue
            
            if start_date <= item_date <= end_date:
                filtered_data.append(item)
    
    return filtered_data

def get_data_summary(data_list, key_field='type'):
    """Get summary statistics for data."""
    summary = {}
    for item in data_list:
        key = item.get(key_field, 'Unknown')
        summary[key] = summary.get(key, 0) + 1
    return summary 