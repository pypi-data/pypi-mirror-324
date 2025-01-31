# -*- coding: utf-8 -*-
"""
@author: nzupp
"""
import numpy as np
from .ex2 import multiple

def add_one(number):
    new_number = multiple(number)
    return new_number + 1

def subtract_one(number):
    new_number = multiple(number)
    return new_number - 1