# -*- coding: utf-8 -*-
"""
@author: nzupp

Unit tests for the random walk implementation
"""

import unittest
from slim_gym.sfs import SFSGym

class TestRandomWalk(unittest.TestCase):
    
    def test_random_walk_completion(self):
        """Test if random walk completes successfully"""
        from random_walk import run_random_agent
        
        env = SFSGym(
            output_file='test_random.slim',
            init_mutation_rate=1e-7,
            num_sites=999,
            recomb_rate=1e-8,
            pop_size=10000,
            sampled_individuals=25,
            sfs_stack_size=8,
            bottleneck=0.98
        )
        
        # Just test that it runs without error
        try:
            run_random_agent(episodes=2, steps_per_episode=10, env=env)
            self.assertTrue(True)  # If we got here, no errors occurred
        finally:
            env.close()

def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()