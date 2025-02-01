import requests
import subprocess
import sys
import os
import time
from packaging import version
from xml.etree import ElementTree as ET

class PyPiUpdater:
    def __init__(self, package_name, local_version, log_path, update_interval_seconds=20 * 3600):
        """
        Initialize PyPiUpdater.

        :param package_name: Name of the package on PyPI.
        :param local_version: Currently installed version.
        :param log_path: Path to the update log file (txt file).
        :param update_interval_seconds: Seconds to wait before update is allowed again (default: 20 hours).
        """
        self.package_name = package_name
        self.local_version = version.parse(local_version)
        self.log_path = log_path
        self.update_interval = update_interval_seconds

    def _get_latest_version(self):
        """Fetch the latest version from PyPI RSS feed."""
        rss_url = f"https://pypi.org/rss/project/{self.package_name.lower()}/releases.xml"

        try:
            response = requests.get(rss_url, timeout=5)
            response.raise_for_status()
            root = ET.fromstring(response.content)

            latest_version = root.find(".//item/title").text.strip()
            return latest_version, None
        except requests.exceptions.RequestException as e:
            return None, f"Network error: {str(e)}"
        except Exception as e:
            return None, f"Error parsing feed: {str(e)}"

    def check_for_update(self, force = False):
        """Check if an update is available."""

        if not force and not self.should_check_for_update():
            return None, "Checked too recently"

        latest_version, error = self._get_latest_version()
        if latest_version is None:
            return None, error

        is_newer = version.parse(latest_version) > self.local_version
        if is_newer:
            self.record_update_check()  # Save the check timestamp only if successful
        return is_newer, latest_version

    def update_package(self):
        """Update the package using pip."""
        print(f"Updating {self.package_name}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", self.package_name], check=True)
            return True, f"{self.package_name} updated successfully."
        except subprocess.CalledProcessError as e:
            return False, f"Update failed: {str(e)}"

    def restart_program(self):
        """Restart the Python program after an update."""
        print("Restarting the application...")
        python = sys.executable
        subprocess.run([python] + sys.argv)
        sys.exit()

    def last_update_check(self):
        """Retrieve the last update check timestamp from a text file."""
        if not os.path.exists(self.log_path):
            return 0  # If no log, assume a long time passed

        try:
            with open(self.log_path, "r") as f:
                last_check = float(f.readline().strip())  # Read first line as timestamp
                return last_check
        except Exception:
            return 0  # Handle read errors gracefully

    def last_update_date_string(self):
        time_float = self.last_update_check()
        local_time = time.localtime(time_float)
        time_string = f"{local_time.tm_mday:02d}/{local_time.tm_mon:02d} {local_time.tm_hour:02d}:{local_time.tm_min:02d}"
        return time_string

    def record_update_check(self):
        """Save the current time as the last update check timestamp."""
        with open(self.log_path, "w") as f:
            f.write(f"{time.time()}")

    def should_check_for_update(self):
        """Returns True if enough time has passed since the last check."""
        last_check = self.last_update_check()
        elapsed_time = time.time() - last_check
        return elapsed_time >= self.update_interval
