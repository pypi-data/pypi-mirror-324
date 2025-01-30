#!/usr/bin/env python3 # for running the script like ./python_file_name.py
# -*_ coding: utf-8 -*-
'''
Entry point for the API/Python Program
'''

# Package Metadata
__author__ = "Girija Golla"         # required
__credits__ = ["Girija Golla"]      # required
__maintainer__ = "Girija Golla"     # Optional
__email__ = "girija.golla@ibm.com"  # required
__status__ = "Development"          # required
__version__ = "0.0.1"               # required

import logging


class LPARActivation:
    '''
    LPAR activation using ZHMCCLI Library.
    '''
    def __init__(self):
        '''
        Constructor.
        Args: None
        Returns: None
        '''
        print("***********Constructor***********")

    def func(self):
        '''
        Constructor.
        Args: None
        Returns: None
        '''
        print("***********func***********")
        logging.info("Hello")


if __name__ == "__main__":
    LPARActivation().func()
