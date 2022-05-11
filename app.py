from curses import raw
from email.mime import image
from json import load
import os

from pickle import NONE, TRUE
from turtle import width
import pygame
from pygame.locals import *

def load_image(file_name, convert_alpha=False):
    image = pygame.image.load(f'images/{file_name}')
    if convert_alpha:
        image.set_colorkey(image.get_at((0, 0)))
        image.convert_alpha()

    return image

class Entity(pygame.sprite.Sprite):

    def __init__(self):
        self.facing = 'R'

        self.image_sets = {}
        self.facing_to_images = None
        self.images = None
        self.image = None
        self.rect = None

        self.frames_per_image = 6
        self.frame_idx = 0

        self.n_images = None
        self.image_idx = 0

        self.image = load_image(file_name, True)
        self.rect = self.image.get_rect()

    def add_images(self, name, file_name, n_images, image_order=None):
        raw_images = load_image(file_name, True)

        *_, width, height = raw_images.get_rect()
        gap = (width - height * n_images) // (n_images - 1)

        images = [
            raw_images.subsurface((height + gap) * idx, 0, height, height)
            for idx in range(n_images)
        ]
        if image_order:
            image_frames = len(images) // len(image_order)
            facing_to_images = {
                direction: images[idx: idx+image_frames]
                for direction, idx in zip(
                    image_order, range(0, n_images, n_images // len(image_order))
                )
            }
        else:
            image_frames = len(images)
            facing_to_images = None

        self.image_sets[name] = images, facing_to_images, image_frames

    def set_images(self, name):
        self.images, self.facing_to_images, self.n_images = self.image_sets[name]
        self.image = self.images[0]
        self.frame_idx = 0
        self.image_idx = 0

    def set_rect(self):
        self.rect = self.image.get_rect()

    def draw(self, surface):
        self.frame_idx += 1
        if self.frame_idx == self.frames_per_image:
            self.frame_idx = 0
            self.image_idx += 1

        if self.image_idx == self.n_images:
            self.image_idx = 0 

        if self.facing_to_images is not None:
            self.image = self.facing_to_images[self.facing][self.image_idx]
        else:
            self.image = self.images[self.image_idx]

        surface.blit(self.image, self.rect)

os.environ['SDL_VIDEO_WINDOW_POS'] =  '1080,30'
pygame.init()

map_image = load_image('map.png')
_, _, WIDTH, HEIGHT = map_image.get_rect()

display = pygame.display.set_mode((WIDTH, HEIGHT))
# 0 - empty, 1 - small_dot, 2 - big_dot, 3 - wall, 4 - pink wall
tiles = [
	[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
	[3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
	[3, 2, 3, 3, 3, 1, 3, 3, 3, 1, 3, 1, 3, 3, 3, 1, 3, 3, 3, 2, 3],
	[3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3],
	[3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
	[3, 1, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 1, 3],
	[3, 1, 3, 3, 3, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 3, 3, 3, 1, 3],
	[3, 1, 1, 1, 1, 1, 3, 3, 3, 0, 3, 0, 3, 3, 3, 1, 1, 1, 1, 1, 3],
	[3, 3, 3, 3, 3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 3, 1, 3, 3, 3, 3, 3],
	[3, 3, 3, 3, 3, 1, 3, 0, 3, 4, 4, 4, 3, 0, 3, 1, 3, 3, 3, 3, 3],
	[3, 3, 3, 3, 3, 1, 3, 0, 3, 0, 0, 0, 3, 0, 3, 1, 3, 3, 3, 3, 3],
	[0, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0],
	[3, 3, 3, 3, 3, 1, 3, 0, 3, 3, 3, 3, 3, 0, 3, 1, 3, 3, 3, 3, 3],
	[3, 3, 3, 3, 3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 3, 1, 3, 3, 3, 3, 3],
	[3, 3, 3, 3, 3, 1, 3, 0, 3, 3, 3, 3, 3, 0, 3, 1, 3, 3, 3, 3, 3],
	[3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
	[3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3],
	[3, 2, 1, 1, 3, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 3, 1, 1, 2, 3],
	[3, 3, 3, 1, 3, 1, 3, 1, 3, 3, 3, 3, 3, 1, 3, 1, 3, 1, 3, 3, 3],
	[3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3],
	[3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 3],
	[3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 3],
	[3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
	[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]
TILE_WIDTH, TILE_HEIGHT = WIDTH // len(tiles[0]), HEIGHT // len(tiles)

FPS = 60
clock = pygame.time.Clock()

pac_man = Entity()
pac_man.add_images('alive', 'pac_man.png', 8, ('R', 'U', 'L', 'D'))
pac_man.set_images('alive')
pac_man.set_rect()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == ord('w'):
                pac_man.facing = 'U'
            elif event.key == ord('a'):
                pac_man.facing = 'L'
            elif event.key == ord('s'):
                pac_man.facing = 'D'
            elif event.key == ord('d'):
                pac_man.facing = 'R'
    
    display.blit(map_image, (0, 0))

    pac_man.draw(display)

    pygame.display.update()
    clock.tick(FPS)