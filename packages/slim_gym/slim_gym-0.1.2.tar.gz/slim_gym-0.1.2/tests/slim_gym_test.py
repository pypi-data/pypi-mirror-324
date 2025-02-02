# -*- coding: utf-8 -*-
"""
@author: nzupp

Some basic unit testing for SLiM-Gym, this will need to be expanded out over time
"""

import unittest
import numpy as np
import os
import subprocess
import tempfile
from slim_gym.sfs import SFSGym

class TestSLiMInstallation(unittest.TestCase):
    
    def test_slim_installed(self):
        """Verify SLiM is available in the system"""
        try:
            result = subprocess.run(['slim', '-v'], 
                                 capture_output=True, 
                                 text=True)
            self.assertEqual(result.returncode, 0)
        except FileNotFoundError:
            self.fail("SLiM is not installed or not in PATH")
    
    def test_slim_script_execution(self):
        """Test basic SLiM script execution"""
        script_content = '''
    initialize() {
        initializeMutationRate(1e-7);
        initializeMutationType("m1", 0.5, "f", 0.0);
        initializeGenomicElementType("g1", m1, 1.0);
        initializeGenomicElement(g1, 0, 999);
        initializeRecombinationRate(1e-8);
    }
    1 early() { sim.addSubpop("p1", 100); }
    10 late() { sim.simulationFinished(); }
        '''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.slim', delete=False) as f:
            try:
                f.write(script_content)
                f.close()  # Close file before executing
                result = subprocess.run(['slim', f.name], 
                                     capture_output=True, 
                                     text=True)
                self.assertEqual(result.returncode, 0, 
                               f"SLiM execution failed with error: {result.stderr}")
            finally:
                try:
                    os.remove(f.name)
                except:
                    pass  # Best effort cleanup

class TestSFSGymEnvironment(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment with default parameters"""
        self.params = {
            'output_file': 'test_sim.slim',
            'init_mutation_rate': 1e-7,
            'num_sites': 999,
            'recomb_rate': 1e-8,
            'pop_size': 10000,
            'sampled_individuals': 25,
            'sfs_stack_size': 8,
            'bottleneck': 0.98
        }
        self.env = SFSGym(**self.params)

    def tearDown(self):
        """Clean up after tests"""
        self.env.close()
        if os.path.exists(self.params['output_file']):
            try:
                os.remove(self.params['output_file'])
            except:
                pass

    def test_env_initialization(self):
        """Test environment initialization"""
        state, _ = self.env.reset()  # Get initial state to verify setup worked
        self.assertIsNotNone(state)
        # Test space dimensions
        expected_bins = 2 * self.params['sampled_individuals']
        self.assertEqual(state.shape, (self.params['sfs_stack_size'], expected_bins))

    def test_reset(self):
        """Test environment reset"""
        state, _ = self.env.reset()
        expected_bins = 2 * self.params['sampled_individuals']
        self.assertEqual(state.shape, (self.params['sfs_stack_size'], expected_bins))
        self.assertTrue(np.all(state >= 0))

    def test_step_action_space(self):
        """Test action space constraints"""
        self.env.reset()
        # Test valid action
        state, reward, terminated, truncated, info = self.env.step(self.env.action_space.sample())
        self.assertIsInstance(reward, float)
        self.assertIsInstance(terminated, bool)
        self.assertIsInstance(truncated, bool)
        self.assertIsInstance(info, dict)

def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()