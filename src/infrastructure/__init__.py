from .adb_manager import ADBManager

# Global instance for the application
# Architect Note: This ensures we maintain a single ADB session
adb_manager = ADBManager()
