import pygame
from configuration import *

class Head_node(pygame.sprite.Sprite):
    def __init__(self, pos, display_surf, groups):
        super().__init__(groups)
        self.spawn_pos = pos
        self.direction = pygame.Vector2()
        self.speed = 150
        self.size = (NODE_PARAMS['DIAMETER'], NODE_PARAMS['DIAMETER'])

        self.image = pygame.Surface(self.size)
        self.image.set_colorkey("black")
        pygame.draw.circle(self.image, "white", NODE_PARAMS['RADIUSXRADIUS'], NODE_PARAMS['DIAMETER']/2, NODE_PARAMS['WIDTH'])
        pygame.draw.circle(self.image, "red", NODE_PARAMS['RADIUSXRADIUS'], 4, 4)

        self.rect = self.image.get_frect(center=self.spawn_pos)

        self.display_surf = display_surf

    def draw(self):
        self.display_surf.blit(self.image, self.rect)

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        dont_move = False
        if abs(mouse_pos[0] - self.rect.centerx) < 0.1 and abs(mouse_pos[1] - self.rect.centery) < 0.1:
            dont_move = True
        else:
            self.direction.x = mouse_pos[0] - self.rect.centerx
            self.direction.y = mouse_pos[1] - self.rect.centery
            self.direction = self.direction.normalize() if self.direction else self.direction

        if not dont_move:
            self.rect.center += self.direction * self.speed * dt
        self.draw()


class Body_node(Head_node):
    def __init__(self, pos, display_surf, groups):
        super().__init__(pos, display_surf, groups)

        # self.head_pos = head_pos
        self.distance_vector = pygame.Vector2()

        # self.distance_vector[0] = self.rect.centerx - head_pos[0]
        # self.distance_vector[1] = self.rect.centery - head_pos[1]
        # self.distance_vector = self.distance_vector.normalize() * 32

        # self.rect.centerx = self.distance_vector[0] + head_pos[0]
        # self.rect.centery = self.distance_vector[1] + head_pos[1]

    def get_head_pos(self, head_pos):
        self.head_pos = head_pos

    def update(self, dt):
        self.distance_vector[0] = self.rect.centerx - self.head_pos[0]
        self.distance_vector[1] = self.rect.centery - self.head_pos[1]
        self.distance_vector = self.distance_vector.normalize() * NODE_PARAMS['DIAMETER']/2 if self.distance_vector else self.distance_vector

        self.rect.centerx = self.distance_vector[0] + self.head_pos[0]
        self.rect.centery = self.distance_vector[1] + self.head_pos[1]


pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Anim')
running = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

node1 = Head_node((500, 500), display_surface, all_sprites)
node2 = Body_node((0,0), display_surface, all_sprites)
node3 = Body_node((0, 0), display_surface, all_sprites)
node4 = Body_node((0, 0), display_surface, all_sprites)

while running:

    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    display_surface.fill("darkblue")

    node2.get_head_pos(node1.rect.center)
    node3.get_head_pos(node2.rect.center)
    node4.get_head_pos(node3.rect.center)
    all_sprites.update(dt)

    all_sprites.draw(display_surface)

    pygame.display.update()

    # print(node2.rect.center)

pygame.quit()