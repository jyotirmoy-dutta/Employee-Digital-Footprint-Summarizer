import platform
import psutil
import os
from datetime import datetime, timedelta

def get_app_usage():
    """Return a list of app usage events for the current user, cross-platform."""
    system = platform.system()
    if system == 'Windows':
        return _get_app_usage_windows()
    elif system == 'Darwin':
        return _get_app_usage_macos()
    elif system == 'Linux':
        return _get_app_usage_linux()
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")

def _get_app_usage_windows():
    """Collect app usage events on Windows."""
    app_usage = []
    
    # Get currently running processes
    try:
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'create_time', 'cpu_percent', 'memory_percent']):
            try:
                proc_info = proc.info
                if proc_info['exe']:  # Only processes with executable path
                    app_usage.append({
                        'name': proc_info['name'],
                        'path': proc_info['exe'],
                        'pid': proc_info['pid'],
                        'start_time': datetime.fromtimestamp(proc_info['create_time']),
                        'cpu_percent': proc_info['cpu_percent'],
                        'memory_percent': proc_info['memory_percent'],
                        'type': 'running_process',
                        'source': 'psutil'
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"Error getting running processes: {e}")
    
    # Get installed applications from registry
    try:
        import winreg
        
        # 64-bit applications
        reg_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        for reg_path in reg_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    install_date = winreg.QueryValueEx(subkey, "InstallDate")[0] if winreg.QueryValueEx(subkey, "InstallDate") else None
                                    
                                    app_usage.append({
                                        'name': display_name,
                                        'path': subkey_name,
                                        'install_date': install_date,
                                        'type': 'installed_app',
                                        'source': 'registry'
                                    })
                                except (FileNotFoundError, OSError):
                                    continue
                        except (FileNotFoundError, OSError):
                            continue
            except (FileNotFoundError, OSError):
                continue
    except Exception as e:
        print(f"Error reading installed apps: {e}")
    
    # Sort by timestamp (most recent first)
    app_usage.sort(key=lambda x: x.get('start_time', datetime.min), reverse=True)
    
    return app_usage

def _get_app_usage_macos():
    """Collect app usage events on macOS (stub)."""
    return []

def _get_app_usage_linux():
    """Collect app usage events on Linux (stub)."""
    return [] 