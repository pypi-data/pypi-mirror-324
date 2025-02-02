import requests
import subprocess
import sys
import os
import time
import json
from packaging import version
from xml.etree import ElementTree as ET

class PyPiUpdater:
    def __init__(self, package_name, local_version, log_path):
        """
        Initialize PyPiUpdater.

        :param package_name: Name of the package on PyPI.
        :param local_version: Currently installed version.
        :param log_path: Path to the update log file (JSON file).
        :param update_interval_seconds: Seconds to wait before update is allowed again (default: 20 hours).
        """
        self.package_name = package_name
        self.local_version = version.parse(local_version)
        self.log_path = log_path
        self.latest_version = ""
        self.last_update_check = 0.1

    def _get_latest_version(self):
        """Fetch the latest version from PyPI RSS feed."""
        rss_url = f"https://pypi.org/rss/project/{self.package_name.lower()}/releases.xml"

        try:
            response = requests.get(rss_url, timeout=5)
            response.raise_for_status()
            root = ET.fromstring(response.content)

            latest_version = root.find(".//item/title").text.strip()
            self.latest_version = latest_version
            return [latest_version, None]
        except requests.exceptions.RequestException as e:
            return [None, f"Network error: {str(e)}"]
        except Exception as e:
            return [None, f"Error parsing feed: {str(e)}"]

    def check_for_update(self):
        """Check if an update is available."""
        latest_version, error = self._get_latest_version()
        if latest_version is None:
            return [None, error]

        is_newer = version.parse(latest_version) > self.local_version
        self._record_update_check()  # Save check timestamp & latest version
        return [is_newer, latest_version]

    def update_package(self):
        """Update the package using pip."""
        print(f"Updating {self.package_name}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", self.package_name], check = True)
            return [True, f"{self.package_name} updated successfully."]
        except subprocess.CalledProcessError as e:
            return [False, f"Update failed: {str(e)}"]

    def restart_program(self):
        """Restart the Python program after an update."""
        print("Restarting the application...")
        python = sys.executable
        subprocess.run([python] + sys.argv)
        sys.exit()

    def get_last_state(self):
        """Retrieve last update info for the package."""
        data = self._read_json()
        if self.package_name in data:
            entry = data[self.package_name]
            return [entry["last_checked"], entry["last_online_version"], self.package_name]
        return [None, None, self.package_name]

    def _record_update_check(self):
        """Save the last update check time and online version in JSON."""
        data = self._read_json()
        data[self.package_name] = {
            "last_checked": time.time(),
            "last_online_version": self.latest_version
        }
        self._write_json(data)

    def clear_all_entries(self):
        """Clear all update history."""
        self._write_json({})

    def _read_json(self):
        """Read JSON log file."""
        if not os.path.exists(self.log_path):
            return {}
        try:
            with open(self.log_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_json(self, data):
        """Write data to JSON log file."""
        with open(self.log_path, "w") as f:
            json.dump(data, f, indent=4)
