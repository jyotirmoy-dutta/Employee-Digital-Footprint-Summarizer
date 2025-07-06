import platform
import os
import psutil
from datetime import datetime, timedelta
import glob

def get_file_shares():
    """Return a list of file shares accessed by the current user, cross-platform."""
    system = platform.system()
    if system == 'Windows':
        return _get_file_shares_windows()
    elif system == 'Darwin':
        return _get_file_shares_macos()
    elif system == 'Linux':
        return _get_file_shares_linux()
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")

def _get_file_shares_windows():
    """Collect file shares accessed on Windows."""
    file_shares = []
    
    # Get recent files from Windows Recent folder
    try:
        recent_path = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Recent")
        if os.path.exists(recent_path):
            for file in os.listdir(recent_path):
                file_path = os.path.join(recent_path, file)
                if os.path.isfile(file_path):
                    try:
                        stat = os.stat(file_path)
                        file_shares.append({
                            'path': file,
                            'timestamp': datetime.fromtimestamp(stat.st_mtime),
                            'type': 'recent_file',
                            'source': 'recent_folder'
                        })
                    except Exception:
                        continue
    except Exception as e:
        print(f"Error reading recent files: {e}")
    
    # Get network drives (simplified approach)
    try:
        # Check for common network drive letters
        for drive in ['Z:', 'Y:', 'X:', 'W:', 'V:', 'U:', 'T:', 'S:', 'R:', 'Q:', 'P:', 'O:', 'N:', 'M:', 'L:', 'K:', 'J:', 'I:', 'H:', 'G:', 'F:', 'E:', 'D:']:
            if os.path.exists(drive):
                try:
                    stat = os.stat(drive)
                    file_shares.append({
                        'path': drive,
                        'timestamp': datetime.fromtimestamp(stat.st_mtime),
                        'type': 'network_drive',
                        'source': 'drive_check'
                    })
                except Exception:
                    continue
    except Exception as e:
        print(f"Error getting network drives: {e}")
    
    # Get shared folders from registry (simplified)
    try:
        import winreg
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    file_shares.append({
                        'path': subkey_name,
                        'timestamp': datetime.now(),
                        'type': 'mounted_share',
                        'source': 'registry'
                    })
                except Exception:
                    continue
    except Exception as e:
        print(f"Error reading registry: {e}")
    
    # Sort by timestamp (most recent first)
    file_shares.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return file_shares

def _get_file_shares_macos():
    """Collect file shares accessed on macOS (stub)."""
    return []

def _get_file_shares_linux():
    """Collect file shares accessed on Linux (stub)."""
    return [] 