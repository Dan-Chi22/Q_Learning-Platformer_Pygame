import pygame
import numpy as np

pygame.init()

# Setting up the game window and clock
screen_w = 1200
screen_h = 800
clock = pygame.time.Clock()

# Define tile size for the game grid
tile_size = 50
screen = pygame.display.set_mode((screen_w, screen_h))
text_font = pygame.font.SysFont("Arial", 20)

# Load sounds
collision_sound = pygame.mixer.Sound("smb2_sound_damage.wav")
jumping_sound = pygame.mixer.Sound("smb3_sound_jump.wav")
background_sound = pygame.mixer.Sound("Theme_Song.mp3")
background_sound.play(-1)

# Define list to store game world elements
world_borders = []

def create_world(data):
    row_count = 0
    for row in data:
        column_count = 0
        for column in row:
            if column == 1:
                border = pygame.image.load("player.jpg") 
                border_img = pygame.transform.scale(border, (tile_size, tile_size))
                border_rect = border_img.get_rect()
                border_rect.x = column_count * tile_size
                border_rect.y = row_count * tile_size
                world_borders.append((border_img, border_rect))
            elif column == 2:
                wall = pygame.image.load("wall.png")
                wall_img = pygame.transform.scale(wall, (tile_size, tile_size))
                wall_rect = wall_img.get_rect()
                wall_rect.x = column_count * tile_size
                wall_rect.y = row_count * tile_size
                world_borders.append((wall_img, wall_rect))
            column_count += 1
        row_count += 1
                

def draw_world():
    for borders in world_borders:
        screen.blit(borders[0], borders[1])

# Define player attributes
player_img = pygame.image.load("little-bear-idle.png")
player = pygame.transform.scale(player_img, (40, 60))
player_width = player.get_width()
player_height = player.get_height()
player_rect = player.get_rect()
player_rect.x = 50
player_rect.y = screen_h - 130
velocity_y = 0
acceleration = 1
jumped = False
direction = 1
last_direction = 1
player_x = player_rect.x
player_y = player_rect.y

# Define enemy attributes
enemy_img = pygame.image.load("alien.png")
enemy_img2 = pygame.image.load("ufo.png")
enemy = pygame.transform.scale(enemy_img, (tile_size, tile_size))
enemy2 = pygame.transform.scale(enemy_img2, (tile_size,tile_size))
enemy2_rect = enemy2.get_rect()
enemy_rect = enemy.get_rect()
enemy_rect.x = 700
enemy_rect.y = 100
enemy2_rect.x = 100
enemy2_rect.y = 250
enemy_x = 1
enemy2_x = 1

# Define exit (goal) attributes
exit_game = pygame.image.load("door.png")
exits = pygame.transform.scale(exit_game, (tile_size, tile_size))
exit_game_rect = exits.get_rect()
exit_game_rect.x = 50
exit_game_rect.y = 100

# Define coin attributes
coin_img = pygame.image.load("yuan.png")
coin = pygame.transform.scale(coin_img, (tile_size, tile_size))
coin_rect = coin.get_rect()
coin_rect.x = 600
coin_rect.y = 250
score = 0
coin_visible = True

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
    
    return reward, get_state()

def update_player(action):
    global player, velocity_y, jumped, direction, last_direction, player_x, player_y

    change_x = 0
    change_y = 0

    if action == 0:  # Move left
        change_x -= 4
        direction = -1
    if action == 1:  # Move right
        change_x = 4
        direction = 1
    if action == 2:  # Jump
        if not jumped:
            jumping_sound.play()
            velocity_y = -15
            jumped = True
    if action == 3:  # Do nothing
        pass

    velocity_y += acceleration
    if velocity_y > 10:
        velocity_y = 10

    change_y += velocity_y

    for tile in world_borders:
        if tile[1].colliderect(player_rect.x, player_rect.y + change_y, player_width, player_height):
            if velocity_y < 0:
                change_y = 0
                velocity_y = 0
            elif velocity_y >= 0:
                change_y = 0
                velocity_y = 0
        if tile[1].colliderect(player_rect.x + change_x, player_rect.y, player_width, player_height):
            change_x = 0

    player_rect.x += change_x 
    player_rect.y += change_y

    if direction != last_direction:
        player = pygame.transform.flip(player, True, False)
        last_direction = direction

    screen.blit(player, player_rect)

def update_enemy():
    global enemy_rect, enemy_x, enemy2_rect, enemy2_x

    enemy_rect.x += enemy_x
    enemy2_rect.x += enemy2_x

    for border in world_borders:
        if border[1].colliderect(enemy2_rect):
            enemy2_x = 0.9
        elif enemy2_rect.x >= 350:
            enemy2_x = -0.9
    if enemy_rect.x <= 400:
        enemy_x = 0.9
    elif enemy_rect.x >= 1000:
        enemy_x = -0.9

    if enemy_rect.colliderect(player_rect):
        collision_sound.play()
        player_rect.x = player_x
        player_rect.y = player_y
    if enemy2_rect.colliderect(player_rect):
        collision_sound.play()
        player_rect.x = player_x
        player_rect.y = player_y


    screen.blit(enemy, enemy_rect)
    screen.blit(enemy2, enemy2_rect)

def exits_update():
    global exit_game_rect, running 

    if exit_game_rect.colliderect(player_rect):
        running = False
    
    screen.blit(exits, exit_game_rect)

def coin_update():
    global coin, coin_rect, coin_visible, score

    if coin_rect.colliderect(player_rect):
        coin_visible = False
        score += 1
        coin_rect.x = -1  

    if not coin_visible:
        while True:
            coin_rect.x = np.random.randint(0, (screen_w // tile_size)) * tile_size
            coin_rect.y = np.random.randint(0, (screen_h // tile_size)) * tile_size

            collision = False
            for tile in world_borders:
                if tile[1].colliderect(coin_rect):
                    collision = True
                    break

            if not collision:
                break

        coin_visible = True

    if enemy_rect.colliderect(player_rect) or enemy2_rect.colliderect(player_rect):
        collision_sound.play()
        player_rect.x = player_x
        player_rect.y = player_y
        if not coin_visible:
            score -= 1
            coin_visible = True

    if coin_visible:
        screen.blit(coin, coin_rect)

#background image
background_img = pygame.image.load("background.png")


world_data = [ 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    
]

create_world(world_data)

# Game loop
running = True
while running:
    dt = clock.tick(60)
    screen.blit(background_img, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_world()
    
    # AI agent's turn
    current_state = get_state()
    action = select_action(current_state)

    update_player(action)

    # Simulate the game, get the reward and new state
    reward, new_state = train_game()

    # Update Q-table based on the reward and the new state
    update_q_table(prev_state, prev_action, reward, new_state)

    # Store current state and action for the next iteration
    prev_state = current_state
    prev_action = action

    score_text = text_font.render('Score: ' + str(score), True, (255, 255, 255))  
    screen.blit(score_text, (50, 50))

    # Simulate the game forward
    update_enemy()
    exits_update()
    coin_update()

    pygame.display.update()

pygame.quit()
