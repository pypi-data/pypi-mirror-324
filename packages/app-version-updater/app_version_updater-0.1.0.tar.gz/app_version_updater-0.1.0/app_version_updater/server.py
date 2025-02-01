from pathlib import Path
from standarted_logger.logger import Logger
from os import listdir
import re
from app_version_updater.models import UpdaterException
import os

class UpdaterServer:
    __validate_expression_default = r'\d+.\d+.\d.[a-z]+'


    def __init__(self, client_version_path = None, use_logger=False, 
                 module_name="client-updater", log_level=10, log_dir=None, console_handler=True,
                 validate_expression: None | str = None):
        
        self.validate_expression = validate_expression

        if client_version_path is None:
            self.client_version_path = Path(".") / "client_versions"
            if not self.client_version_path.exists():
                self.client_version_path.mkdir(parents=True, exist_ok=True)
        else:
            self.client_version_path = client_version_path
        
        self.logger = Logger.get_logger(module_name, log_level, log_dir, console_handler) if use_logger else None

    def app_version(self):
        try:
            return self.__find_latest_version().encode()
        except FileNotFoundError:
            raise UpdaterException("404 No client update")

    def app(self, version: str):
        try:
            file = self.__get_file_by_version(version)
        except FileNotFoundError:
            raise UpdaterException("403 Client required app version that does not exist")
        return file

    def __find_latest_version(self):
        """Among content of client_version_path find the file with 
        the greates version in the name"""
        filenames = self.__get_folder_content()
        if not filenames:
            raise FileNotFoundError("No client updates")
        max_version = "0.0.0"
        for file_name in filenames:
            try:
                max_version = max(max_version, file_name)
            except Exception as e:
                if self.logger is not None:
                    self.logger.info(f"Invalid client_update file name")
        return max_version


    def __get_file_by_version(self, version: str) -> Path:
        for file in listdir(self.client_version_path):
            if not self.__is_file_valid(file):
                continue
            if self.__split_extension(file) == version:
                return Path(self.client_version_path) / Path(file)
        raise FileNotFoundError(f"File with the {version=} is not found or not valid")
    
    def __get_folder_content(self):
        """return valid client_update files without extensions"""
        filenames = [self.__split_extension(f) \
                    for f in listdir(os.path.join(Path(os.getcwd()), self.client_version_path)) \
                        if self.__is_file_valid(f)]
        return filenames
    
    def __is_file_valid(self, file_name: str):
        if self.validate_expression is None:
            validate_expression = UpdaterServer.__validate_expression_default

        if re.match(validate_expression, file_name) is None:
            return False
        return (Path(self.client_version_path) / Path(file_name)).exists()
    
    def __split_extension(self, file_name: str):
        """Remove extension from file. Doesn't verify if the file exists"""
        file_path = Path(self.client_version_path) / Path(file_name)
        return  file_path.stem