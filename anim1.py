import pygame
from configuration import *
from creature_classes import Head_node, FISH_node, LIZARD_node


pygame.init()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Anim')
running = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
body_nodes_sprites = pygame.sprite.Group()
head_nodes_sprites = pygame.sprite.Group()


def create_fish(creature_length, creature_body_array):
    Head_node((500, 500), display_surface, creature_body_array[0], 300, (all_sprites, head_nodes_sprites))
    for i in range(1, creature_length):
        FISH_node((0, 0), display_surface, creature_body_array[i], 300, (all_sprites, body_nodes_sprites))

def create_lizard(creature_length, creature_body_array):
    Head_node((500, 500), display_surface, creature_body_array[0], 150, (all_sprites, head_nodes_sprites))
    for i in range(1, creature_length):
        if creature_body_array[i] == 30: # node with a leg
            LIZARD_node((0, 0), display_surface, creature_body_array[i], 150, (all_sprites, body_nodes_sprites), has_legs=True)
        else: # node without a leg
            LIZARD_node((0, 0), display_surface, creature_body_array[i], 150, (all_sprites, body_nodes_sprites))

def random_body_shape(): #TODO
    pass
    # TODO random creation of interesting creatures:
    # import numpy as np
    # samples = np.random.lognormal(mean=3.5, sigma=0.4, size=14).astype(int)
    # creature_body_array2 = (sorted(samples, reverse=True))

    # creature_body_array = [52, 58, 40, 60, 68, 71, 65, 50, 28, 19, 21, 13, 13, 7, 25]
    # creature_body_array = [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25]

# MY_CREATURE = "Fish"
MY_CREATURE = "Lizard"

if MY_CREATURE == "Fish":
    # FISH 
    creature_body_array = [40, 55, 54, 40, 25, 15, 10]
    create_fish(len(creature_body_array), creature_body_array)

if MY_CREATURE == "Lizard":
    # LIZARD
    creature_body_array = [35, 25, 30, 25, 25, 25, 30, 20, 15, 10, 10, 5]
    create_lizard(len(creature_body_array), creature_body_array)

while running:

    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    display_surface.fill("darkblue")

    for node, its_head in zip(body_nodes_sprites, all_sprites):
        node.get_head_pos(its_head.rect.center)
        node.get_head_direction(its_head.direction) # TODO do better angle constraint
        
    dots_coords = []
    dots_coords1 = []
    dots_coords2 = []

    for head in head_nodes_sprites: # Draw the dots / get body-shape points position
        head.draw_dots(1, 0, display_surface, "red", dots_coords1, dots_coords2, yesAppend=True) # draw 0° peak-dot
        for sign in [1, -1]:
            degrees = 45
            head.draw_dots(sign, degrees, display_surface, "red", dots_coords1, dots_coords2, yesAppend=True) # draw +- 45° dots
            head.draw_dots(sign, 90, display_surface, "white", dots_coords1, dots_coords2, yesAppend=False) # draw the eyes

    for node in all_sprites:
        for sign in [1, -1]:
            degrees = 90
            node.draw_dots(sign, degrees, display_surface, "red", dots_coords1, dots_coords2, yesAppend=True) # draw +- 90° dots
    
    if MY_CREATURE == "Fish": # Draw the side-fins 
        for node in body_nodes_sprites:    
            if node.size == (55,55):
                for sign in [1, -1]:
                    node.draw_fins(sign, 55, 25)
            if node.size == (25,25):
                for sign in [1, -1]:
                    node.draw_fins(sign, 30, 10)

    dots_coords2.reverse()
    dots_coords = dots_coords + dots_coords1 + dots_coords2
    # pygame.draw.lines(display_surface, "red", True, dots_coords) # Draw the body shape NOT filled    

    all_sprites.update(dt)

    pygame.draw.polygon(display_surface, "red", dots_coords) # Draw the body shape filled

    if MY_CREATURE == "Fish": # Draw the tail-fins
        for node in body_nodes_sprites: 
            if node.size == (10,10):
                for head in head_nodes_sprites:
                    node.draw_tailfin(head.rect.center, 50, 8)
            if node.size == (54,54):
                for head in head_nodes_sprites:
                    node.draw_tailfin(head.rect.center, 60, 6)

    # Draw eyes
    for head in head_nodes_sprites:
        for sign in [1, -1]:
            head.draw_dots(sign, 90, display_surface, "white", dots_coords1, dots_coords2, yesAppend=False) # draw the eyes

    body_nodes_sprites.draw(display_surface)

    pygame.display.update()


pygame.quit()
