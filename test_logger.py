#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
<ENTER DESCRIPTION HERE>
"""
from k_util.logger import Logger

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"
__version__ = "0.0.0"

if __name__ == "__main__":
    Logger.header("Running Tools Test")
    Logger.field("Version", "1.2.0")
    Logger.log("Hello World")
    Logger.line_break()