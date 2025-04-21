import pygame
from configuration import *
from math import sin, cos, acos, radians, degrees as math_degrees

class Head_node(pygame.sprite.Sprite):
    def __init__(self, pos, display_surf, size, groups):
        super().__init__(groups)
        self.spawn_pos = pos
        self.direction = pygame.Vector2(1,1).normalize()
        self.prev_direction = pygame.Vector2()
        self.speed = 250
        self.size = (size, size)
        # trying with different circle diameters AND different rect sizes
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey("black")

        # pygame.draw.circle(self.image, "white", (size/2, size/2), size/2, NODE_PARAMS['WIDTH']) # draw the circle-skeleton
        # pygame.draw.circle(self.image, "white", (size/2, size/2), 4, 4) # draw the dots-skeleton

        self.rect = self.image.get_frect(center=self.spawn_pos)

        self.display_surf = display_surf #TODO we have it in here xd

    def rotate_vector(self, vector_to_rotate, sign, degrees):
        theta = radians(sign*degrees)
        rotated_V = (vector_to_rotate.x * cos(theta) - vector_to_rotate.y * sin(theta), vector_to_rotate.x * sin(theta) + vector_to_rotate.y * cos(theta))
        rotated_V = pygame.Vector2(rotated_V[0], rotated_V[1])
        return rotated_V

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
        # pygame.draw.circle(display_surface, color, (rotated0, rotated1), 4, 4)
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
            vectors_differece_offset = 0.9 # hardcoded value! 0.6 for snake

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

    def draw_curve(self, start_point, control_point, end_point):
        steps = 50
        prev = start_point
        for i in range(1, steps + 1):
            t = i / steps
            # Quadratic Bezier formula
            point = (1 - t)**2 * start_point + 2 * (1 - t) * t * control_point + t**2 * end_point
            pygame.draw.aaline(self.display_surf, "white", prev, point)
            prev = point

    def draw_fins(self, sign, fin_length, fin_width):

        rotated_Vector1 = self.rotate_vector(self.direction, sign, 130)
        fin_center0 = (self.rect.centerx + (rotated_Vector1.x)*self.size[0]/2)
        fin_center1 = (self.rect.centery + (rotated_Vector1.y)*self.size[0]/2)
        # pygame.draw.circle(self.display_surf, "green", (fin_center0, fin_center1), 4, 4) # draw the center of the fin

        fin_top0 = self.rect.centerx # top and bottom
        fin_top1 = self.rect.centery
        fin_endpoint0 = (self.rect.centerx + (rotated_Vector1.x)*fin_length*5/4)
        fin_endpoint1 = (self.rect.centery + (rotated_Vector1.y)*fin_length*5/4)
        if fin_top1 > fin_endpoint1:
            fin_rect_top = pygame.Vector2(fin_endpoint0, fin_endpoint1)
            fin_rect_bottom = pygame.Vector2(fin_top0, fin_top1)
        else:
            fin_rect_top = pygame.Vector2(fin_top0, fin_top1)
            fin_rect_bottom = pygame.Vector2(fin_endpoint0, fin_endpoint1)

        rotated_Vector2 = self.rotate_vector(rotated_Vector1, 1, 90)
        rotated_Vector3 = self.rotate_vector(rotated_Vector1, -1, 90)

        fin_left0 = (fin_center0 + (rotated_Vector2.x)*fin_width) # left and right
        fin_left1 = (fin_center1 + (rotated_Vector2.y)*fin_width)
        fin_right0 = (fin_center0 + (rotated_Vector3.x)*fin_width) 
        fin_right1 = (fin_center1 + (rotated_Vector3.y)*fin_width) 
        if fin_left0 > fin_right0:
            fin_rect_left = pygame.Vector2(fin_right0, fin_right1)
            fin_rect_right = pygame.Vector2(fin_left0, fin_left1)
        else:
            fin_rect_left = pygame.Vector2(fin_left0, fin_left1)
            fin_rect_right = pygame.Vector2(fin_right0, fin_right1)

        # fin_coords = [fin_rect_left, fin_rect_top, fin_rect_right, fin_rect_bottom] # "sharp fins"
        # pygame.draw.lines(self.display_surf, "white", True, fin_coords)

        self.draw_curve(fin_rect_top, fin_rect_right, fin_rect_bottom)
        self.draw_curve(fin_rect_top, fin_rect_left, fin_rect_bottom)

    def draw_tailfin(self, head_center, fin_length, fin_width):
        # tailfin_offset = abs(self.direction.angle_to(self.head_direction)) TODO figure out how to use the %body_curvature

        rotated_Vector1 = self.rotate_vector(self.direction, 1, 180)
        fin_top0 = self.rect.centerx # top and bottom
        fin_top1 = self.rect.centery
        fin_endpoint0 = (self.rect.centerx + (rotated_Vector1.x)*fin_length)
        fin_endpoint1 = (self.rect.centery + (rotated_Vector1.y)*fin_length)
        fin_center0 = (self.rect.centerx + (rotated_Vector1.x)*fin_length/2)
        fin_center1 = (self.rect.centery + (rotated_Vector1.y)*fin_length/2)

        fin_rect_top = pygame.Vector2(fin_top0, fin_top1)
        fin_rect_bottom = pygame.Vector2(fin_endpoint0, fin_endpoint1)

        rotated_Vector2 = self.rotate_vector(self.direction, 1, 90)
        fin_control_point0 = (fin_center0 + (rotated_Vector2.x)*fin_width)
        fin_control_point1 = (fin_center1 + (rotated_Vector2.y)*fin_width)
        fin_rect_control_point = pygame.Vector2(fin_control_point0, fin_control_point1)

        fin_control_point20 = (fin_center0 - (rotated_Vector2.x)*fin_width)
        fin_control_point21 = (fin_center1 - (rotated_Vector2.y)*fin_width)
        fin_rect_control_point2 = pygame.Vector2(fin_control_point20, fin_control_point21)

        tail_head_vector = pygame.Vector2()
        tail_head_vector.x = head_center[0] - fin_endpoint0
        tail_head_vector.y = head_center[1] - fin_endpoint1
        tail_head_vector = tail_head_vector.normalize() if tail_head_vector else tail_head_vector
        
        fin_rect_bottom += 10*tail_head_vector

        self.draw_curve(fin_rect_top, fin_rect_control_point, fin_rect_bottom)
        self.draw_curve(fin_rect_top, fin_rect_control_point2, fin_rect_bottom)
        # pygame.draw.circle(self.display_surf, "green", (fin_center0, fin_center1), 4, 4) # draw the center of the fin

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

# creature_body_array = [52, 58, 40, 60, 68, 71, 65, 50, 28, 19, 21, 13, 13, 7, 25]
# creature_body_array = [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25]

# FISH TODO
creature_body_array = [40, 55, 54, 40, 25, 15, 10]
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

    # Draw the dots / get body-shape points position
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

    
    for node in body_nodes_sprites: # Draw the side-fins    
        if node.size == (55,55):
            for sign in [1, -1]:
                node.draw_fins(sign, 55, 25)
        if node.size == (25,25):
            for sign in [1, -1]:
                node.draw_fins(sign, 30, 10)


    dots_coords2.reverse()
    dots_coords = dots_coords + dots_coords1 + dots_coords2
    # pygame.draw.lines(display_surface, "red", True, dots_coords) # Draw the body shape
    pygame.draw.polygon(display_surface, "red", dots_coords) # Draw the body shape filled


    for node in body_nodes_sprites: # Draw the tail-fins
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

    all_sprites.update(dt)

    body_nodes_sprites.draw(display_surface)

    pygame.display.update()


pygame.quit()
