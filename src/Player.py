import pygame

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
