# -*- coding: utf-8 -*-

import os
import random
import uuid
from unittest import TestCase
from k_util.serializable import Serializable, decode_decorator_with_version

__version__ = "1.2.3"
TARGET_FILE = "data.json"


class CustomData(Serializable):
    """ This is an example sub-class of the Serializable. """

    K1 = "key1"
    K2 = "key2"
    K3 = "key3"
    K4 = "key4"
    K5 = "key5"

    def __init__(self):
        self.key1: str = uuid.uuid4().hex
        self.key2: int = random.randint(1000, 9999)
        self.key3: float = random.random()
        self.key4: dict = {"a": 1, "b": 2}
        self.key5: list = [1, 2, 3]

    def encode(self) -> dict:
        data = {
            self.S_VERSION_KEY: __version__,
            self.K1: self.key1,
            self.K2: self.key2,
            self.K3: self.key3,
            self.K4: self.key4,
            self.K5: self.key5,
        }
        return data

    @staticmethod
    @decode_decorator_with_version(__version__)
    def decode(data: dict) -> 'CustomData':
        custom_data = CustomData()
        custom_data.key1 = data[CustomData.K1]
        custom_data.key2 = data[CustomData.K2]
        custom_data.key3 = data[CustomData.K3]
        custom_data.key4 = data[CustomData.K4]
        custom_data.key5 = data[CustomData.K5]
        return custom_data


class TestSerializable(TestCase):

    def setUp(self):
        self.all_keys = [
            CustomData.K1,
            CustomData.K2,
            CustomData.K3,
            CustomData.K4,
            CustomData.K5,
        ]

    def tearDown(self):
        if os.path.exists(TARGET_FILE):
            os.remove(TARGET_FILE)

    def test_can_serialize(self):
        """ Can initialize and encode a custom data. """
        custom_data = CustomData()
        data = custom_data.encode()

        for k in self.all_keys:
            self.assertTrue(k in data)

    def test_decode_decorator(self):
        """ Test if the decode decorator functions as intended. """

        # Attempting to decode a null object should return None.
        result = CustomData.decode(None)
        self.assertEqual(None, result)

        # Attempting to decode an object without a version key should fail.
        with self.assertRaises(Exception):
            CustomData.decode({})

        # Attempting to decode an object without a version key should fail.
        with self.assertRaises(Exception):
            CustomData.decode({Serializable.S_VERSION_KEY: "0.0.0"})

    def test_decode(self):
        """ Serialized data can be encoded and decoded back into its original value. """
        c1 = CustomData()
        data = c1.encode()
        c2 = CustomData.decode(data)
        self.check_data_equality(c1, c2)

    def test_write_file(self):
        """ Can save the encoded data as JSON file. The data can be read back in. """
        c1 = CustomData()
        c1.write_to_file(TARGET_FILE)

        # The file has been written.
        self.assertTrue(os.path.exists(TARGET_FILE))

        # File can be read back into data form.
        c2 = CustomData.load_from_file(TARGET_FILE)
        self.check_data_equality(c1, c2)

    def check_data_equality(self, c1: CustomData, c2: CustomData):
        """ Check if the data from two objects are equal. """
        self.assertEqual(c1.key1, c2.key1)
        self.assertEqual(c1.key2, c2.key2)
        self.assertEqual(c1.key3, c2.key3)
        self.assertSequenceEqual(c1.key4, c2.key4)
        self.assertSequenceEqual(c1.key5, c2.key5)

    def test_abstract_methods(self):
        """ Abstract methods can be called without error. """
        custom_data = Serializable()

        # Encoding should be a dictionary type.
        data = custom_data.encode()
        self.assertEqual(dict, type(data))

        # Just see if we can call it without blowing up.
        _ = Serializable.decode(data)




