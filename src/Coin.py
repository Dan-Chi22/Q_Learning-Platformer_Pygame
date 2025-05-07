import pygame

# Define coin attributes
coin_img = pygame.image.load("yuan.png")
coin = pygame.transform.scale(coin_img, (tile_size, tile_size))
coin_rect = coin.get_rect()
coin_rect.x = 600
coin_rect.y = 250
score = 0
coin_visible = True

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
