# -*- coding: utf-8 -*-
"""
@author: nzupp

Reference env for SLiM-Gym reinforcement learning framework

Extends four key functions
1) Process initial state
2) Process state
3) Process action
4) Calculate reward

In this env, we define our observations, our actions, and how we evaluate those
actions. An overview of the env can be found in the associated paper.
"""

import numpy as np
from gymnasium import spaces
from collections import deque
from .slim_gym import SLiMGym
from .slim_injector import create_slim_script

class SFSGym(SLiMGym):
    def __init__(self, 
                 output_file,
                 init_mutation_rate,
                 num_sites,
                 recomb_rate,
                 pop_size,
                 sampled_individuals,
                 sfs_stack_size,
                 bottleneck):
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
        
        # Create the SLiM script first
        # Calls to the SLiM injector
        create_slim_script(
            output_file=output_file,
            init_mutation_rate=init_mutation_rate,
            num_sites=num_sites,
            recomb_rate=recomb_rate,
            pop_size=pop_size,
            sample_size=sampled_individuals,
            bottleneck=bottleneck
        )
    
        # Initialize base class with generated script
        super().__init__(slim_file=output_file)
        
        self.init_mutation_rate = init_mutation_rate
        self.current_mutation_rate = init_mutation_rate
        self.num_sites = num_sites
        self.num_bins = (sampled_individuals * 2)
        self.sfs_stack_size = sfs_stack_size
        self.expectation_sfs = None
        
        # Action space that allows for some parameter of the simulation to be
        # controlled. The current env allows for discrete control of mutation rate,
        # either by increasing it, decreasing it or staying the same.
        self.action_space = spaces.Discrete(3)
        self.action_map = {
            0: 0.9,
            1: 1.0,
            2: 1.1
        }

        # We define the observation space as the SFS of the simulation at each
        # generation. The number of bins in the SFS is equal to the number of 
        # diploid individuals times two.
        self.observation_space = spaces.Box(
            low=0,
            high=self.num_sites,
            shape=(self.sfs_stack_size, self.num_bins),
            dtype=np.float64
        )
        
        # We also implement 'SFS stacking', similar to frame stacking, to extend
        # conext in training
        self.sfs_stack = deque(maxlen=sfs_stack_size)
        self.initialize_sfs_stack()

    def initialize_sfs_stack(self):
        """
        Code to initalize the starting SFS stack
        
        Params:
            None

        Returns:
            Nothing
        """
        self.sfs_stack.clear()
        for _ in range(self.sfs_stack_size):
            # Near zero probability in initalized SFS. This is consistent with SLiM;
            # view their documentations for details on how they init pops
            noise = np.full(self.num_bins, 1e-10)
            self.sfs_stack.append(noise)

    # The data passed from SLiM is not immediately in SFS format- in fact it is in MS format
    # (Note: This format can be changed in either the .slim script or SLiM injector)
    def get_sfs(self, state_data):
        """
        Code to extract

        Params
            state_data (SLiM MS format): The output SLiM in MS format

        Returns
            sfs (np.ndarray)
        """
        lines = state_data.strip().split('\n')
        binary_lines = [line.strip() for line in lines 
                       if set(line.strip()).issubset({'0', '1'})]
        # Small postive val for KLD calc later- applied to all instances
        if not binary_lines:
            return np.zeros(self.num_bins, dtype=np.float32) + 1e-10
        
        lengths = [len(line) for line in binary_lines]
        max_len = max(lengths)
        binary_lines = [line.ljust(max_len, '0')[:max_len] for line in binary_lines]
        
        data = np.array([[int(char) for char in line] for line in binary_lines])
        column_sums = np.sum(data, axis=0)
        
        sfs = np.zeros(self.num_bins, dtype=np.float32) + 1e-10
        values, counts = np.unique(column_sums, return_counts=True)
        
        for val, count in zip(values, counts):
            if val < len(sfs):
                sfs[val] = count + 1e-10
                
        return sfs
    
    def get_expectation_sfs(self, state_data):
        """
        Use log data from our burn in to set an expectation SFS before any Ne modification

        Params
            state_data (SLiM MS format): The output of the SLiM in MS format

        Returns
            Nothing
        """
        ms_entries = state_data.strip().split('\n\n')
        all_sfs = []
        
        for entry in ms_entries:
            sfs = self.get_sfs(entry)
            all_sfs.append(sfs)
        
        if all_sfs:
            self.expectation_sfs = all_sfs

    def process_state(self, state_data):
        """
        Implement the abstract SLiM-Gym function. If its the first step we get the
        expectation SFS, otherwise we just call to get_sfs and dequeue the SFS stack

        Params
            state_data (SLiM MS format): The output of SLiM in MS format

        Returns
            sfs_stack (np.ndarray)

        """
        if self.step_count == 1:
            self.get_expectation_sfs(state_data)
            
        new_sfs = self.get_sfs(state_data)
        self.sfs_stack.append(new_sfs)
        return np.stack(list(self.sfs_stack))

    def process_action(self, action):
        """
        Implement the abstract SLiM-Gym function by assigning a new mutation rate.
        Note: mutation rate is bound between 1e-8 and 1e-6, which could be too restrictive

        Params
            action (Int): Discrete action of 0, 1 or 2

        Returns
            new_rate (Float): The modified mutation rate
        """
        multiplier = self.action_map[action]
        new_rate = np.clip(
            self.current_mutation_rate * multiplier,
            1e-8,
            1e-6
        )
        self.current_mutation_rate = new_rate
        return str(new_rate)

    # TODO I imagine this could be the center of a decent experiment
    def calculate_reward(self, state, action, next_state):
        """
        Implements the abstract SLiM-Gym function 'calculate_reward'. We test how divergent our current SFS is
        from each SFS in our expectation, to get an overall divergence. The negative divergence
        is then applied as the reward, with learning algorithms working to maximize reward i.e.
        minimize divergence

        Params
            state (np.ndarray): A stack of SFS of SFS_stack_size size
            action (Float): Float multiplier to apply to our mutation rate
            next_state (np.ndarray): The resulting state after applying the action

        Returns
            reward (Float): Negative mean KL divergence between current SFS and expectation SFS.
        """
        try:
            current_sfs = next_state[-1] + 1e-10
            
            klds = []
            for exp_sfs in self.expectation_sfs:
                exp_sfs = np.array(exp_sfs) + 1e-10
                
                current_normalized = current_sfs / np.sum(current_sfs)
                expectation_normalized = exp_sfs / np.sum(exp_sfs)
                
                kld = np.sum(expectation_normalized * (
                    np.log(expectation_normalized) - np.log(current_normalized)))
                
                if np.isfinite(kld):
                    klds.append(kld)
            
            # Big negative for errors
            if not klds:
                print("Warning: No valid KLD calculations")
                return -100000.0
            
            return float(-np.mean(klds))
            
        except Exception as e:
            print(f"Error in reward calculation: {e}")
            return -10000.0
    
    def get_initial_state(self):
        """
        Implement the abstract SLiM-Gym function by initalizing the sfs stack

        Returns
            (np.ndarray): Initial sfs stack
        """
        self.initialize_sfs_stack()
        return np.stack(list(self.sfs_stack))