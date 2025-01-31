import requests
from packaging import version

class PyPiUpdateCheck:

    def _get_latest_version_from_rss(self, package_name):
        """
        Fetch the RSS feed from PyPI and extract the latest version number.
        Returns the latest version or None if an error occurs.
        """
        rss_url = f"https://pypi.org/rss/project/{package_name.lower()}/releases.xml"

        try:
            response = requests.get(rss_url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

            # Extract the latest version from the RSS XML
            # The RSS feed is XML, so we just need to parse the version from the first entry
            from xml.etree import ElementTree as ET
            root = ET.fromstring(response.content)

            # The version is in the <title> tag of the first <item> in the RSS feed
            latest_version = root.find(".//item/title").text.strip()
            return latest_version, None
        except requests.exceptions.RequestException as e:
            return None, f"Network error: {str(e)}"
        except Exception as e:
            return None, f"Error parsing feed: {str(e)}"

    def _compare_versions(self, local_version, online_version):
        """
        Compare the local and online version strings.
        Returns (True, online_version) if online is newer, (False, online_version) if same or older.
        """
        try:
            local_ver = version.parse(local_version)
            online_ver = version.parse(online_version)

            if online_ver > local_ver:
                return True, online_version  # Online version is newer
            else:
                return False, online_version  # Local version is the same or newer
        except Exception as e:
            return None, f"Error comparing versions: {str(e)}"

    def check_for_update(self, package_name, local_version):
        """
        Check if the given package has a newer version on PyPI compared to the local version.
        Returns (True, online_version), (False, online_version), or (None, error_message).
        """
        online_version, error_message = self._get_latest_version_from_rss(package_name)

        if online_version is None:
            return None, error_message  # Error fetching or parsing feed

        return self._compare_versions(local_version, online_version)
