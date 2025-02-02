# -*- coding: utf-8 -*-
"""
@author: nzupp

SLiM-Gym: A gymnasium environment for SLiM evolutionary simulations
"""

__version__ = "0.2.0"

from .slim_gym_wrapper import SLiMGym
from .sfs import SFSGym
from .slim_injector import create_slim_script
from .examples.make_env import make_env
from .examples.SB3_PPO import train_agent
from .examples.random_walk import run_random_agent

__all__ = [
    'SLiMGym',
    'SFSGym',
    'create_slim_script',
    'run_random_agent',
    'make_env',
    'train_agent'
]