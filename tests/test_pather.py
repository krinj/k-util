# -*- coding: utf-8 -*-

import os
import shutil
from unittest import TestCase
from k_util import pather

BASIC_PATH = "basic"
TWO_LEVEL_PATH = "two/level"
FILE_DIRECTORY_SHORT = "hello"
FILE_DIRECTORY_LONG = FILE_DIRECTORY_SHORT + "/world"
FILE_PATH = FILE_DIRECTORY_LONG + "/file.txt"


class TestPather(TestCase):

    def tearDown(self):
        all_paths = [BASIC_PATH, TWO_LEVEL_PATH, FILE_DIRECTORY_LONG, FILE_PATH]
        for p in all_paths:
            root_path = p.split("/")[0]
            if os.path.exists(root_path):
                shutil.rmtree(root_path)

    def test_create_path(self):
        pather.create(BASIC_PATH)
        self.assertEqual(True, os.path.exists(BASIC_PATH))

    def test_create_nested_path(self):
        pather.create(TWO_LEVEL_PATH)
        self.assertEqual(True, os.path.exists(TWO_LEVEL_PATH))

    def test_create_file_path(self):
        pather.create(FILE_PATH)
        self.assertEqual(True, os.path.exists(FILE_DIRECTORY_LONG))

    def test_path_clearing(self):
        """ Create a path with a bunch of files, and then clear them. """
        pather.create(FILE_DIRECTORY_LONG)
        n_files_1 = 10
        n_files_2 = 5

        for i in range(n_files_1):
            with open(f"{FILE_DIRECTORY_LONG}/file_{i}.txt", "w") as f:
                f.write(str(i))

        # Files are there.
        self.assertEqual(n_files_1, len(os.listdir(FILE_DIRECTORY_LONG)))

        for i in range(n_files_2):
            with open(f"{FILE_DIRECTORY_SHORT}/file_{i}.txt", "w") as f:
                f.write(str(i))

        # Clear the directory and see that the tail files are gone.
        pather.create(FILE_DIRECTORY_LONG, clear=True)
        self.assertEqual(0, len(os.listdir(FILE_DIRECTORY_LONG)))

        # The other files should still be there.
        self.assertEqual(n_files_2, len([f for f in os.listdir(FILE_DIRECTORY_SHORT) if "txt" in f]))

    def test_create_root_path(self):
        """ Creating root path should immediately return. """
        pather.create("/")
