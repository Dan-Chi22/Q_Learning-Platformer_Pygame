import pygame

# Define exit (goal) attributes
exit_game = pygame.image.load("door.png")
exits = pygame.transform.scale(exit_game, (tile_size, tile_size))
exit_game_rect = exits.get_rect()
exit_game_rect.x = 50
exit_game_rect.y = 100

def exits_update():
    global exit_game_rect, running 

    if exit_game_rect.colliderect(player_rect):
        running = False
    
    screen.blit(exits, exit_game_rect)
