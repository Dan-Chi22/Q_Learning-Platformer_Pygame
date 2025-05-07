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
background_sound.play(-1) #background image
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
