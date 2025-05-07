import pygame
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
