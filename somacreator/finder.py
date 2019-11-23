import os
import fnmatch


class WSDLFinder:
    def __init__(self, path):
        self.wsdl_info_dict = {}
        self.path = path

    def add_wsdl_info(self, path):
        for dirpath, dirnames, files in os.walk(path):
            for file_name in files:
                if fnmatch.fnmatch(file_name, '*.wsdl'):
                    self.wsdl_info_dict[file_name] = dirpath
