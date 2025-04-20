import pygame
from configuration import *
from math import sin, cos, acos, radians, degrees as math_degrees

class Head_node(pygame.sprite.Sprite):
    def __init__(self, pos, display_surf, size, groups):
        super().__init__(groups)
        self.spawn_pos = pos
        self.direction = pygame.Vector2(1,1).normalize()
        self.prev_direction = pygame.Vector2()
        self.speed = 150
        self.size = (size, size)
        # trying with different circle diameters AND different rect sizes
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey("black")

        # pygame.draw.circle(self.image, "white", (size/2, size/2), size/2, NODE_PARAMS['WIDTH']) # draw the circle-skeleton
        # pygame.draw.circle(self.image, "white", (size/2, size/2), 4, 4) # draw the dots-skeleton

        self.rect = self.image.get_frect(center=self.spawn_pos)

        self.display_surf = display_surf

    def draw(self):
        self.display_surf.blit(self.image, self.rect)

    def draw_dots(self, sign, degrees, display_surface, color, dots_coords1, dots_coords2, yesAppend):
        theta = radians(sign*degrees)
        rotated_V = (self.direction.x * cos(theta) - self.direction.y * sin(theta), self.direction.x * sin(theta) + self.direction.y * cos(theta))
        if yesAppend:
            rotated0 = (self.rect.centerx + (rotated_V[0])*self.size[0]/2)
            rotated1 = (self.rect.centery + (rotated_V[1])*self.size[0]/2)
        else: # drawing the eyes
            rotated0 = (self.rect.centerx + (rotated_V[0])*self.size[0]/4)
            rotated1 = (self.rect.centery + (rotated_V[1])*self.size[0]/4)
        pygame.draw.circle(display_surface, color, (rotated0, rotated1), 4, 4)
        if yesAppend:
            if sign == 1:
                dots_coords1.append((rotated0, rotated1))
            else:
                dots_coords2.append((rotated0, rotated1))

    def update(self, dt):

        dont_move = False
        mouse_pos = pygame.mouse.get_pos() if pygame.mouse.get_pos() != (0,0) else (WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # if pygame.mouse.get_pressed()[0]:
        #     dont_move = False

        self.prev_direction = self.direction.copy()

        if abs(mouse_pos[0] - self.rect.centerx) < (10+self.size[0]/2) and abs(mouse_pos[1] - self.rect.centery) < (10+self.size[1]/2):
            dont_move = True
        
        self.direction.x = mouse_pos[0] - self.rect.centerx
        self.direction.y = mouse_pos[1] - self.rect.centery
        self.direction = self.direction.normalize() if self.direction else self.direction

        # smooth-out changing the direction
        vectors_differece = 10*(self.direction - self.prev_direction)

        if vectors_differece.length() < 1:
            vectors_differece_offset = 0.8 # hardcoded value!
        else:
            vectors_differece_offset = 0.6 # hardcoded value!

        self.direction.x = ((self.direction.x/10)*vectors_differece_offset + (self.prev_direction.x*10)/vectors_differece_offset)
        self.direction.y = ((self.direction.y/10)*vectors_differece_offset + (self.prev_direction.y*10)/vectors_differece_offset)
        self.direction = self.direction.normalize() if self.direction else self.direction

        if not dont_move:
            self.rect.center += self.direction * self.speed * dt
        
        self.draw()

class Body_node(Head_node):
    def __init__(self, pos, display_surf, size, groups):
        super().__init__(pos, display_surf, size, groups)
        self.direction = pygame.Vector2()
        self.size = (size, size)
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey("black")
        self.theta = 0
        self.cross = 0
        # pygame.draw.circle(self.image, "white", (size/2, size/2), size/2, NODE_PARAMS['WIDTH']) # circle of this node
        # pygame.draw.circle(self.image, "white", (size/2, size/2), 4, 4) # center of this node

        self.rect = self.image.get_frect(center=self.spawn_pos)

    def get_head_pos(self, head_pos):
        self.head_pos = head_pos

    def get_head_direction(self, head_direction):
        self.head_direction = head_direction
        self.angle_constraint()
    
    def angle_constraint(self):
        # calculate angle between node's and its head's vectors
        dot = self.direction.x * self.head_direction.x + self.direction.y * self.head_direction.y
        cos_theta = dot / (1 * 1) # lengths of vectors
        cos_theta = max(min(cos_theta, 1), -1)
        self.theta = math_degrees(acos(cos_theta))
        
    def update(self, dt):
        
        self.direction.x =  self.head_pos[0] - self.rect.centerx # vectors from this node to its head
        self.direction.y =  self.head_pos[1] - self.rect.centery
        self.direction = self.direction.normalize() if self.direction else self.direction

        # angle constraint
        if abs(self.theta) > 45:
            self.direction.x = (self.direction.x*80 + self.head_direction.x/80)
            self.direction.y = (self.direction.y*80 + self.head_direction.y/80)
            self.direction = self.direction.normalize() if self.direction else self.direction
        # 

        self.distance_vector = -self.direction * 32 # vector from head to this node (*32 -> The nodes are spread evenly)


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
head_nodes_sprites = pygame.sprite.Group()


def create_creature(creature_length, creature_body_array):
    Head_node((500, 500), display_surface, creature_body_array[0], (all_sprites, head_nodes_sprites))
    for i in range(1, creature_length):
        Body_node((0, 0), display_surface, creature_body_array[i], (all_sprites, body_nodes_sprites))

# TODO random creation of interesting creatures:
# import numpy as np
# samples = np.random.lognormal(mean=3.5, sigma=0.4, size=14).astype(int)
# creature_body_array2 = (sorted(samples, reverse=True))

creature_body_array = [52, 58, 40, 60, 68, 71, 65, 50, 28, 19, 21, 13, 13, 7, 25]
# creature_body_array = [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25]
create_creature(len(creature_body_array), creature_body_array)

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

    for head in head_nodes_sprites:
        head.draw_dots(1, 0, display_surface, "red", dots_coords1, dots_coords2, yesAppend=True) # draw 0° peak-dot
        for sign in [1, -1]:
            degrees = 45
            head.draw_dots(sign, degrees, display_surface, "red", dots_coords1, dots_coords2, yesAppend=True) # draw +- 45° dots
            head.draw_dots(sign, 90, display_surface, "white", dots_coords1, dots_coords2, yesAppend=False) # draw the eyes

    for node in all_sprites:
        for sign in [1, -1]:
            degrees = 90
            node.draw_dots(sign, degrees, display_surface, "red", dots_coords1, dots_coords2, yesAppend=True) # draw +- 90° dots


    dots_coords2.reverse()
    dots_coords = dots_coords + dots_coords1 + dots_coords2
    pygame.draw.lines(display_surface, "red", True, dots_coords)

    all_sprites.update(dt)

    body_nodes_sprites.draw(display_surface)

    pygame.display.update()


pygame.quit()
