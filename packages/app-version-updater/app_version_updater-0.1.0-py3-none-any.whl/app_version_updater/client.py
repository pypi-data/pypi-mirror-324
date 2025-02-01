from standarted_logger.logger import Logger
import requests
from pathlib import Path
import re
import time

from app_version_updater.models import UpdaterException, UpdaterConnectionError

class UpdaterClient():
    ipv4_pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    def __init__(self, 
                 host: str,                                     # host ip in form http://<ip>
                 host_domain: str,                              # application prefix: /<app>/route1, /<app>/<route2>
                 request_period=600,                            # timeout of requests in seconds
                 use_logger=False,                              # turn on/off logging
                 module_name="client-updater",                  # module name for logger
                 log_level=10,                                  # 10/20...50 or logging.DEBUG
                 log_dir=None,                                  # path to save log files
                 console_handler=True,                          # set False if double logging (TODO: fix later)
                 save_folder: Path = Path.home() / "Downloads"): # directory to save new version's files

        self.HOST = host
        self.host_domain = host_domain
        self.app_request_version_period = request_period
        self.CLIENT_SAVE_FOLDER = save_folder
        self.logger = Logger.get_logger(module_name, log_level, log_dir, console_handler) if use_logger else None


    def manage_app_versions(self, current_app_version, cred) -> None:
        '''
        Main thread that requests newer app versions from server,
        fetches updates (if any) and updates app
        :raises: UpdaterException If new version is downloaded - raise UpdaterException with file name as error message
        :raises: UpdaterConnectionError If the server is unavailable
        '''
        while True:
            try:
                version = self.get_actual_app_version(cred) # Getting only version value
                if self.logger is not None:
                    self.logger.debug(f"Requested actual client version - got {version}")
                if not version:
                    if self.logger is not None:
                        self.logger.debug(f"No client update")
                elif current_app_version < version and version != "None":
                    if self.logger is not None:
                        self.logger.info(f"Downloading version {version}...")
                    app = self.download_new_app(version, cred) # getting in memory, not on disk yet
                    if self.logger is not None:
                        self.logger.info(f"Upgrading to verison {version}, extracting...")
                    self.save_setup_file(app, version) # saving to path on disk
                else:
                    if self.logger is not None:
                        self.logger.debug(f"Latest app version ({version}) matching, no update required")
            except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
                if self.logger is not None:
                    self.logger.warning(f"Connection with server is broken...")
                raise UpdaterConnectionError(f"Connection with server is broken...")

            time.sleep(self.app_request_version_period)

    def save_setup_file(self, content: bytes, version: str):
        # Loads setup (exe) file
        try:
            path = self.CLIENT_SAVE_FOLDER / f'setup_{self.host_domain}_{version.replace(".", "")}.exe'
            if path.exists():
                if path.stat().st_size == len(content):
                    raise FileExistsError("The setup file was already downloaded")
            path.write_bytes(content)
        except FileExistsError:
            if self.logger is not None:
                self.logger.info(f"Downloaded file was already downloaded")
            return
        if self.logger is not None:
            self.logger.info("Client update was downloaded")
        raise UpdaterException(str(path))

    def get_actual_app_version(self, cred) -> str:
        # Getting latest app version from server
        res = requests.get(self.HOST + f"/{self.host_domain}/appVersion", 
                            params={"cred": cred})
            
        if res.status_code == 200:
            return res.content.decode().replace("\"", "")
        if res.status_code == 404:
            return ""
        else:
            raise UpdaterException(f"HTTP {res.status_code} {res.text}")

    def download_new_app(self, new_version: str, cred) -> bytes:
        # Getting FileResponse from server in bytes - needs further writing to disk
        res = requests.get(self.HOST + f"/{self.host_domain}/app", 
                            params={"cred": cred, "version": new_version})
        
        if res.status_code == 200:
            return res.content
        else:
            raise UpdaterException(f"HTTP {res.status_code}") 
