#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Simple mouse class containing position and relative position change
@File      : mouse.py
@Project   : pygletPlayground
@Time      : 13.10.21 19:45
@Author    : flowmeadow
"""
import attr


@attr.s
class Mouse:
    """
    Simple mouse data structure containing position and relative position change
    """
    x: int = attr.ib(default=0)
    y: int = attr.ib(default=0)
    dx: int = attr.ib(default=0)
    dy: int = attr.ib(default=0)
    scroll_dx: int = attr.ib(default=0)
    scroll_dy: int = attr.ib(default=0)
    keys: set = attr.ib(default=set())

    def update_position(self, x: int, y: int, dx: int, dy: int):
        """
        Update attributes
        :param x: x-position
        :param y: y-position
        :param dx: change in x-direction
        :param dy: change in y-direction
        """
        self.x = x
        self.y = y
        self.dx += dx
        self.dy += dy

    def reset(self):
        """
        reset relative change
        """
        self.dx = 0
        self.dy = 0
        self.scroll_dx = 0
        self.scroll_dy = 0

    def update_scroll(self, scroll_x: int, scroll_y: int):
        """
        Update attributes
        :param x: x-position
        :param y: y-position
        :param dx: change in x-direction
        :param dy: change in y-direction
        """
        self.scroll_dx += scroll_x
        self.scroll_dy += scroll_y
