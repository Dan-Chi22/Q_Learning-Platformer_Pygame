# Q-Learning Game using Pygame
This project creates a 2D grid-based Q-Learning algorithm game using Python and Pygame that allows game agent learn and interact with the game environment. 
# Table of Contents
* Project Overview
* AI Approach (Q-Learning)
* Game Elements
* World Setup
* Q-Learning Process
* AI Training Flow
## Project Overview
This project is a 2D grid-based game developed using Python and Pygame, enhanced with Q-Learning—a Reinforcement Learning (RL) algorithm that allows the game agent (player) to learn from interaction with the game environment.
The goal of the player is to:
1. Navigate through a world filled with enemies and obstacles,

2. Collect coins for extra rewards,

3. Avoid negative outcomes like enemy collisions,

4. Reach the exit door (goal) to complete the level.

## AI Approach — Q-Learning
Q-Learning is a model-free RL algorithm that helps the agent learn an optimal policy through trial and error. The agent uses a Q-table to estimate the expected utility of taking an action in a specific state.
## Key Parameters:
1. Learning rate (α): 0.9 — weight given to new experiences.

2. Discount factor (γ): 0.1 — importance of future rewards.

3. Exploration rate (ε): 0.4 — randomness in action selection to balance exploration and exploitation.

## Game Elements
1. Player: The main agent controlled by the Q-learning algorithm.

2. Enemies: Colliding with these results in a negative reward.

3. Coins: Provide a positive reward when collected.

4. Exit Door: Reaching it gives the maximum reward and ends the level.

5. Obstacles/Walls: Static elements that restrict movement.

6. Sounds: Background music, collision, and jumping effects enhance the user experience.

## World Setup
The world is defined by a 2D array where each value represents a specific tile:
* 0: Empty space

* 1: Border or wall

* 2: Ground/Platform

The function create_world() uses this array to place the game elements in the world.

## Q-Learning Process
1. State Representation: Player’s current tile location on the grid (x, y).

2. Action Space: 4 possible actions — left, right, jump, and do nothing.

3. Q-Table Initialization: A 3D NumPy array — [x][y][action].

4. Action Selection: Epsilon-greedy strategy:

* With probability ε, a random action is chosen.

* With probability 1-ε, the best known action is selected.

5. Reward Function:

* +1000 for reaching the goal.

* +100 for collecting a coin.

* +20 for successful jumps.

* -100 for enemy collisions.

6. Q-Value Update: Q(s, a) = (1 - α) * Q(s, a) + α * (r + γ * max(Q(s', a')))

## AI Training Flow
1. Each frame, the training involves:

2. Getting the current state of the agent.

3. Selecting an action using the Q-table policy.

4. Updating the player position using the selected action.

5. Calculating the reward based on the outcome.

6. Updating the Q-table using the update_q_table() method.

## Key Learning Outcomes
1. Integration of game development with AI

2. Application of Q-learning in a real-time environment

3. Understanding of state-action-reward mechanisms

4. Experience with Pygame and NumPy
