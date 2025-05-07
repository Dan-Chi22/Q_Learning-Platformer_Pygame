import pygame

# Q-learning parameters
learning_rate = 0.9
discount_factor = 0.1
epsilon = 0.4

# Q-table initialization
action_space_size = 4  # Number of possible actions (left, right, jump, do nothing)
state_space_size = (screen_w // tile_size, screen_h // tile_size)  # Grid size
q_table = np.zeros((state_space_size[0], state_space_size[1], action_space_size))

# State and action history
prev_state = None
prev_action = None

def get_state():
    return (player_rect.x // tile_size, player_rect.y // tile_size)

def select_action(state):
    if np.random.rand() > epsilon:
       return np.argmax(q_table[state[0], state[1]])
    else:
        return np.random.choice(action_space_size) 

def update_q_table(prev_state, prev_action, reward, new_state):
    if prev_state is not None:
        best_future_reward = np.max(q_table[new_state[0], new_state[1]])
        current_q_value = q_table[prev_state[0], prev_state[1], prev_action]
        print(f"Q-values before update: {q_table[prev_state[0], prev_state[1]]}")
        
        new_q_value = (1 - learning_rate) * current_q_value + learning_rate * (reward + discount_factor * best_future_reward)
        q_table[prev_state[0], prev_state[1], prev_action] = new_q_value

        print(f"Q-values after update: {q_table[prev_state[0], prev_state[1]]}")

def train_game():
    global player_rect, score, jumped

    # Save the current player state
    prev_player_rect = player_rect.copy()

    # Perform actions based on the current Q-table policy
    current_state = get_state()
    action = select_action(current_state)

    print(f"Current state: {current_state}, Chosen action: {action}")

    # Calculate the reward based on the changes in the environment
    reward = 0

    # Check if the player has reached the goal (door)
    if exit_game_rect.colliderect(player_rect):
        reward = 1000  # A positive reward for reaching the goal
        running = False  # End the simulation

    # Check for collisions with enemies or negative events
    if enemy_rect.colliderect(player_rect) or enemy2_rect.colliderect(player_rect):
        reward = -100  # A negative reward for colliding with enemies
        player_rect = prev_player_rect  # Reset the player position

    # Check for coin collection
    if coin_rect.colliderect(player_rect):
        reward = 100  # A small positive reward for collecting a coin
        score += 1

    if action == 2 and jumped:
        reward += 20  # A positive reward
        jumped = False

    print(f"Reward: {reward}, New state: {get_state()}")
    
    return reward, get_state())
