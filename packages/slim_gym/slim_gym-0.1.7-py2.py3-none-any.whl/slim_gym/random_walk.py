from .sfs import SFSGym
import matplotlib.pyplot as plt

def run_random_agent(episodes=5,
                    steps_per_episode=100,
                    plot=True,
                    env=None):
    """
    Runs the random agent.
    
    Params:
        episodes (Int): number of episodes to run the agent for
        steps_per_episode (Int): number of steps agent will take in env per episode
        plot (Bool): Whether or not to plot the rewards over episodes
        env (SLiM-Gym env): The env the agent will act in- defaults to SFSGym
        
    Returns:
        Nothing
    """
    
    if env is None:
        env = SFSGym(
            output_file='sim.slim',
            init_mutation_rate=1e-7,
            num_sites=999,
            recomb_rate=1e-8,
            pop_size=10000,
            sampled_individuals=25,
            sfs_stack_size=8,
            bottleneck=0.98
        )

    # Store step-by-step rewards for each episode
    episode_reward_trajectories = []

    for episode in range(episodes):
        print(f"\nStarting Episode {episode + 1}")
        
        # Reset environment
        state, _ = env.reset()
        cumulative_reward = 0
        episode_rewards = [0]  # Start at 0

        for step in range(steps_per_episode):
            # Random action
            action = env.action_space.sample()
            
            # Take step in environment
            next_state, reward, terminated, truncated, info = env.step(action)
            cumulative_reward += reward
            episode_rewards.append(cumulative_reward)  # Track cumulative reward at each step
            
            print(f"Step {step + 1}: Action {action}, Reward {reward:.4f}")
            
            if terminated or truncated:
                print(f"Episode ended early at step {step + 1}")
                break
        
        episode_reward_trajectories.append(episode_rewards)
        print(f"Episode {episode + 1} total reward: {cumulative_reward:.4f}")

    plot_results(episode_reward_trajectories)
    env.close()

def plot_results(episode_reward_trajectories):
    """
    Plot the step-by-step rewards for each episode.
    
    Params:
        episode_reward_trajectories (List of Lists): The stored reward trajectories for each episode
    
    Returns:
        Nothing
    """
    plt.figure(figsize=(10, 6))
    
    for episode, rewards in enumerate(episode_reward_trajectories):
        plt.plot(rewards, label=f'Episode {episode + 1}')
    
    plt.title('Cumulative Reward per Step')
    plt.xlabel('Step')
    plt.ylabel('Cumulative Reward')
    plt.legend()
    plt.grid(True)
    plt.show()