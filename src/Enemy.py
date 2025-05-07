import pygame

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
