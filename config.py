import ConfigParser
import os


class Config():

    def __init__(self):
        self.__config = ConfigParser.ConfigParser()
        self.__config.read(os.path.join(os.environ['HOME'],
                                        ".config/maximiliano.conf"))

        self.api_endpoint = self.__config.get("config", "api_endpoint")
        self.api_user = self.__config.get("config", "api_user")
        self.api_password = self.__config.get("config", "api_password")

    def get(self, section, option):
        return self.__config.get(section, option)
