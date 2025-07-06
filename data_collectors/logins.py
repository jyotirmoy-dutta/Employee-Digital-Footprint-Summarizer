import platform
import psutil
from datetime import datetime, timedelta
import win32evtlog
import win32evtlogutil
import win32con
import win32security

def get_logins():
    """Return a list of login events for the current user, cross-platform."""
    system = platform.system()
    if system == 'Windows':
        return _get_logins_windows()
    elif system == 'Darwin':
        return _get_logins_macos()
    elif system == 'Linux':
        return _get_logins_linux()
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")

def _get_logins_windows():
    """Collect login events on Windows using psutil."""
    logins = []
    
    # Get current user sessions
    try:
        for session in psutil.users():
            logins.append({
                'timestamp': datetime.fromtimestamp(session.started),
                'username': session.name,
                'host': session.host or 'localhost',
                'type': 'session',
                'source': 'psutil'
            })
    except Exception as e:
        print(f"Error getting sessions: {e}")
    
    # Add current user info
    try:
        current_user = psutil.users()[0] if psutil.users() else None
        if current_user:
            logins.append({
                'timestamp': datetime.now(),
                'username': current_user.name,
                'host': current_user.host or 'localhost',
                'type': 'current',
                'source': 'psutil'
            })
    except Exception as e:
        print(f"Error getting current user: {e}")
    
    # Sort by timestamp (most recent first)
    logins.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return logins

def _get_logins_macos():
    """Collect login events on macOS (stub)."""
    return []

def _get_logins_linux():
    """Collect login events on Linux (stub)."""
    return [] 