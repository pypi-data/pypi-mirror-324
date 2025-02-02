# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 15:55:43 2025

@author: nzupp
"""
import slim_gym

def make_env(output_file='sim.slim',
    init_mutation_rate=1e-7,
    num_sites=999,
    recomb_rate=1e-8,
    pop_size=10000,
    sampled_individuals=25,
    sfs_stack_size=8,
    bottleneck=0.99):
    """
    Initalizes the env.
    
    Params:
        output_file (String): Name of the SLiM script the injector generates. Must end with .slim extension.
        init_mutation_rate (Float): Starting mutation rate of the SLiM simulation
        num_sites (Int): Number of sites to simulate (reccomend under 1k for testing)
        recomb_rate (Float): The recombination rate
        pop_size (Int): The size of the starting poplation. Note: Assume Ne = Nc under WF
        sampled_individuals (Int): number of individuals sampled each step
        SFS_stack_size (Int): Size of SFS 'stack' i.e. how many generations of SFS stay in observation
        bottleneck (Float): The multiplicative factor the population is changed by. When less than 1 bottleneck, greater than 1 is expansion
        
    Returns:
        Nothing       
    """
    
    env = slim_gym.SFSGym(
        output_file=output_file,
        init_mutation_rate=init_mutation_rate,
        num_sites=num_sites,
        recomb_rate=recomb_rate,
        pop_size=pop_size,
        sampled_individuals=sampled_individuals,
        sfs_stack_size=sfs_stack_size,
        bottleneck=bottleneck,
    )
    
    return env