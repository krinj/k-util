# -*- coding: utf-8 -*-

"""
This abstract class creates an interface for its subclasses to be
serialized into JSON dictionary objects, and possibly also written to file.
"""

import json
from abc import abstractmethod

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"
__version__ = "0.0.0"


def decode_decorator_with_version(version: str):
    def decorated_with_version(f):
        def decorated_decoder(data: dict):

            if data is None:
                return None

            if Serializable.S_VERSION_KEY not in data:
                raise Exception("Failed attempt to decode data because the data does not have a version key.")

            data_version = data[Serializable.S_VERSION_KEY]
            if data_version != version:
                raise Exception(f"Failed to decode data: Version mismatch.\n"
                                f"Decoder Version: {version}\n"
                                f"Data Version: {data_version}\n")

            return f(data)

        return decorated_decoder
    return decorated_with_version


class Serializable:

    S_VERSION_KEY = "v"  # Key for the version number of this serialization.

    @abstractmethod
    def encode(self) -> dict:
        """ Convert from this custom data type into a Dictionary. """
        data = {self.S_VERSION_KEY: __version__}
        return data

    @staticmethod
    @abstractmethod
    def decode(data: dict):
        """ Convert from a Dictionary back into this custom data type. """
        pass

    def write_to_file(self, file_path: str) -> None:
        """ Serialize and write the data into a JSON file. """
        data = self.encode()
        with open(file_path, "w") as f:
            json.dump(data, f, indent=1)

    @classmethod
    def load_from_file(cls, file_path: str):
        """ Read and reconstruct the data from a JSON file. """
        with open(file_path, "r") as f:
            data = json.load(f)
            item = cls.decode(data=data)
        return item
