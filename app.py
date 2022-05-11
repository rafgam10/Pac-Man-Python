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

    def draw(self, surface):
        surface.blit(self.image, self.rect)

os.environ['SDL_VIDEO_WINDOW_POS'] =  '1080,30'
pygame.init()

map_image = load_image('map.png')
_, _, WIDTH, HEIGHT = map_image.get_rect()

display = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
clock = pygame.time.Clock()

pac_man = Entity('pac_man.png')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    display.blit(map_image, (0, 0))

    pac_man.draw(display)

    pygame.display.update()
    clock.tick(FPS)