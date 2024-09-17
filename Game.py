"""
Author: Guoxin Wang
Date: 2024-09-17 13:04:35
LastEditors: Guoxin Wang
LastEditTime: 2024-09-17 16:30:27
FilePath: \PoolSolver\Game.py
Description: 

Copyright (c) 2024 by Guoxin Wang, All Rights Reserved. 
"""

import pygame


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Game:
    def __init__(self, current_w, current_h):
        ######## setup ########
        if current_w > current_h:
            self.screen_w = current_w / 5
            self.screen_h = current_w / 5 * 1.624
        else:
            self.screen_w = current_h / 5
            self.screen_h = current_h / 5 * 1.624
        self.grid_w = self.screen_w * 0.854 / 6
        self.offset = Point(self.screen_w * 0.073, self.screen_w * 0.232)

        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.bg = pygame.image.load("assets/bg_default.png")
        self.bg = pygame.transform.scale(self.bg, (self.screen_w, self.screen_h))
        self.frame = pygame.image.load("assets/frame.png")
        self.frame = pygame.transform.scale(self.frame, (self.screen_w, self.screen_h))
        self.fish_nor = pygame.image.load("assets/T1.png")
        self.fish_nor = pygame.transform.scale(
            self.fish_nor, (self.grid_w * 0.7 * 2, self.grid_w * 0.7)
        )

        ######## set all flags ########
        self.solving = False
        self.fish_click = False

    def draw_setup(self):
        # fill the screen with a background image to wipe away anything from last frame
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.frame, (0, 0))

        if self.fish_click:
            pass
        else:
            self.screen.blit(
                self.fish_nor,
                (
                    self.offset.x + self.grid_w * 0.15,
                    self.offset.y + self.grid_w * 0.15,
                ),
            )

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_pos.y -= 300 * self.dt
        if keys[pygame.K_s]:
            self.player_pos.y += 300 * self.dt
        if keys[pygame.K_a]:
            self.player_pos.x -= 300 * self.dt
        if keys[pygame.K_d]:
            self.player_pos.x += 300 * self.dt

        # flip() the display to put all changes on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        self.dt = self.clock.tick(60) / 1000


if __name__ == "__main__":
    pygame.init()
    current_w, current_h = (
        pygame.display.Info().current_w,
        pygame.display.Info().current_h,
    )
    game = Game(current_w, current_h)
    RUN = True
    while RUN:
        # pygame.QUIT event means the user clicked X to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
        if game.solving:
            pass
        else:
            game.draw_setup()
    pygame.quit()
