import math
import pygame


class Obstacle:
    def __init__(self, x, ground_y, speed, width=25, height=40):
        self.x = x
        self.prev_x = x  # where the obstacle was before its latest move
        self.width = width
        self.height = height
        self.y = ground_y - height
        self.speed = speed
        self.scored = False

    def move(self):
        self.prev_x = self.x
        self.x -= self.speed

    def off_screen(self):
        return self.x + self.width < 0

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def swept_rect(self):
        """Rectangle covering everything the obstacle passed through this frame.

        rect() only describes where the obstacle ENDED UP. If it moved further
        than the player is wide in one frame, it could jump over the player and
        never overlap. This one stretches from the new position back to the old
        one so no part of the path is skipped.
        """
        left = math.floor(self.x)
        right = math.ceil(self.prev_x + self.width)
        return pygame.Rect(left, self.y, max(right - left, self.width), self.height)
