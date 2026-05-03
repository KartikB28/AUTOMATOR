import platform
import subprocess


def send_notification(title: str, message: str):
    """Send a desktop notification using system-native methods."""
    try:
        system = platform.system()
        if system == 'Darwin':
            subprocess.run([
                'osascript', '-e',
                f'display notification "{message}" with title "{title}"'
            ], check=False, capture_output=True)
        elif system == 'Linux':
            subprocess.run([
                'notify-send', title, message
            ], check=False, capture_output=True)
        elif system == 'Windows':
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=5, threaded=True)
            except ImportError:
                pass
    except Exception:
        pass
