import pygame
from configuration import *
from math import sin, cos

class Head_node(pygame.sprite.Sprite):
    def __init__(self, pos, display_surf, size, groups):
        super().__init__(groups)
        self.spawn_pos = pos
        self.direction = pygame.Vector2()
        self.speed = 150
        self.size = (size, size)
        # trying with different circle diameters AND different rect sizes
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey("black")
        pygame.draw.circle(self.image, "white", (size/2, size/2), size/2, NODE_PARAMS['WIDTH'])
        pygame.draw.circle(self.image, "red", (size/2, size/2), 4, 4)

        self.rect = self.image.get_frect(center=self.spawn_pos)

        #
        self.dot1_surf = pygame.Surface(self.size)
        self.dot1_surf.set_colorkey("black")
        pygame.draw.circle(self.dot1_surf, "red", (size/2, size/2), 4, 4)
        self.dot1_rect = self.dot1_surf.get_frect(center=self.spawn_pos)
        #


        self.display_surf = display_surf

    def draw(self):
        self.display_surf.blit(self.image, self.rect)
        self.display_surf.blit(self.dot1_surf, self.dot1_rect)

    def draw_dots(self):
        
        rotated0 = (self.rect.centerx + (self.direction[0])*self.size[0]/2)
        rotated1 = (self.rect.centery + (self.direction[1])*self.size[0]/2)
        center0 = (rotated0,rotated1)
        self.dot1_rect.center = center0

    def update(self, dt):
        dont_move = False
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            dont_move = False
        if abs(mouse_pos[0] - self.rect.centerx) < 0.1 and abs(mouse_pos[1] - self.rect.centery) < 0.1:
            dont_move = True
        else:
            self.direction.x = mouse_pos[0] - self.rect.centerx
            self.direction.y = mouse_pos[1] - self.rect.centery
            self.direction = self.direction.normalize() if self.direction else self.direction

        if not dont_move:
            self.rect.center += self.direction * self.speed * dt
        self.draw_dots()
        self.draw()


class Body_node(Head_node):
    def __init__(self, pos, display_surf, size, groups):
        super().__init__(pos, display_surf, size, groups)
        self.direction = pygame.Vector2()
        self.size = (size, size)
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey("black")
        pygame.draw.circle(self.image, "white", (size/2, size/2), size/2, NODE_PARAMS['WIDTH'])
        pygame.draw.circle(self.image, "red", (size/2, size/2), 2, 2)

        self.rect = self.image.get_frect(center=self.spawn_pos)


    def get_head_pos(self, head_pos):
        self.head_pos = head_pos

    def update(self, dt):
        self.direction[0] = self.rect.centerx - self.head_pos[0]
        self.direction[1] = self.rect.centery - self.head_pos[1]
        self.direction = self.direction.normalize() if self.direction else self.direction

        self.distance_vector = self.direction * 32 # The nodes are spread evenly

        self.rect.centerx = self.distance_vector[0] + self.head_pos[0]
        self.rect.centery = self.distance_vector[1] + self.head_pos[1]


pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Anim')
running = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
body_nodes_sprites = pygame.sprite.Group()


def create_creature(creature_length, creature_body_array):
    # max_size_of_node = max(creature_body_array)
    Head_node((500, 500), display_surface, creature_body_array[0], all_sprites)
    for i in range(1, creature_length):
        Body_node((0, 0), display_surface, creature_body_array[i], (all_sprites, body_nodes_sprites))

# TODO random creation of interesting creatures:
# import numpy as np
# samples = np.random.lognormal(mean=3.5, sigma=0.4, size=14).astype(int)
# creature_body_array2 = (sorted(samples, reverse=True))

creature_body_array = [52, 58, 40, 60, 68, 71, 65, 50, 28, 15, 21, 19, 13, 13]
create_creature(len(creature_body_array), creature_body_array)

dots_coords = [] # TODO make a list of the 'dots-coordinates' and connect them with lines

while running:

    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    display_surface.fill("darkblue")


    for node, its_head in zip(body_nodes_sprites, all_sprites):
        node.get_head_pos(its_head.rect.center)


    for node in all_sprites:
        for sign in [1, -1]:
            rotated_V = (-sign*node.direction[1], sign*node.direction[0])
            rotated0 = (node.rect.centerx + (rotated_V[0])*node.size[0]/2)
            rotated1 = (node.rect.centery + (rotated_V[1])*node.size[0]/2)
            pygame.draw.circle(display_surface, "red", (rotated0, rotated1), 4, 4)
        

    all_sprites.update(dt)

    body_nodes_sprites.draw(display_surface)

    pygame.display.update()

    # print(node2.rect.center)

pygame.quit()
