# -*- coding: utf-8 -*-
"""
@author: nzupp

Vanilla, Stable Baselines 3 PPO. Currently, none of these hyperparameters
are tuned, but the initial experiments show learning on the SFS env
"""

import os
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from .make_env import make_env

def train_agent(total_timesteps=50000):
    # Create dirs
    log_dir = "logs"
    model_dir = "models"
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    # Create envs
    env = make_env()
    env = Monitor(env)
    # Initialize PPO
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=128,
        batch_size=32,
        n_epochs=5,
        gamma=0.99,
        tensorboard_log=log_dir
    )

    # Train
    model.learn(
        total_timesteps=total_timesteps,
        progress_bar=True
    )

    model.save(f"{model_dir}/final_model")
    return model

if __name__ == "__main__":
    print("Training agent...")
    model = train_agent()