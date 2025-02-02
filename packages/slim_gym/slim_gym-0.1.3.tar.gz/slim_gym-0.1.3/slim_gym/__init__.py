# -*- coding: utf-8 -*-
"""
@author: nzupp

SLiM-Gym: A gymnasium environment for SLiM evolutionary simulations
"""

__version__ = "0.1.3"

from .slim_gym import SLiMGym
from .sfs import SFSGym
from .slim_injector import create_slim_script
from .random_walk import run_random_agent
