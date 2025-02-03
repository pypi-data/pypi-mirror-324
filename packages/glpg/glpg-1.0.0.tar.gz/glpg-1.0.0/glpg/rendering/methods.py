#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : several methods to draw simple references into a scene
@File      : rendering.py
@Time      : 09.09.21 00:23
@Author    : flowmeadow
"""
from typing import Tuple

import numpy as np
import pyglet
from pyglet.gl import *

from glpg.texturing.texture import Texture


# def draw_text_3D(x_txt: int, y_txt: int, z_txt: int, text: str, color=(1.0, 1.0, 1.0)) -> None:
#     """
#     Draws a given string into the scene.
#     :param x_txt: x-position
#     :param y_txt: y_txt-position
#     :param z_txt: z_txt-position
#     :param text: test to draw
#     :param color: color of the text
#     :return: None
#     """
#     font = GLUT_BITMAP_8_BY_13
#     glColor3f(color[0], color[1], color[2])
#     glRasterPos3f(x_txt, y_txt, z_txt)
#     for ch in text:
#         glutBitmapCharacter(font, ord(ch))


def draw_text_2D(x: int, y: int, text: str, color=(1.0, 1.0, 1.0, 1.0), **kwargs) -> None:
    """
    Draw a text onto the screen
    :param x: x-position
    :param y: y-position
    :param text: text string
    :param color: color of the text; 3 or 4 values (RGB or RGBA)
    :return:
    """
    color = [int(c * 255) for c in color]
    if len(color) == 3:
        color.append(1.0)

    label = pyglet.text.Label(
        text, font_name="Consolas", font_size=12, x=x, y=y, anchor_x="left", anchor_y="top", color=color, **kwargs
    )
    label.draw()


def draw_coordinates(R=np.eye(3), t=np.zeros(3), scale=1.0):
    """
    Draws a reference coordinate system in the scene
    :param R: rotation matrix array (3, 3)
    :param t: center array of the coordinate system (3,)
    :param scale: scale factor
    """
    center = np.array([0.0, 0.0, 0.0]) + t
    vertices = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    colors = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    glBegin(GL_LINES)
    for v, c in zip(vertices, colors):
        v = (R @ v) * scale + t
        glColor3f(*c)
        glVertex3f(*center)
        glVertex3f(*v)
    glEnd()
    glFlush()


def draw_light(light_pos: np.ndarray):
    """
    Draw a reference for a point light source
    :param light_pos: center of the light source (3,)
    :return: None
    """
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(light_pos[0] - 0.1, light_pos[1], light_pos[2])
    glVertex3f(light_pos[0] + 0.1, light_pos[1], light_pos[2])
    glVertex3f(light_pos[0], light_pos[1] - 0.1, light_pos[2])
    glVertex3f(light_pos[0], light_pos[1] + 0.1, light_pos[2])
    glVertex3f(light_pos[0], light_pos[1], light_pos[2] - 0.1)
    glVertex3f(light_pos[0], light_pos[1], light_pos[2] + 0.1)
    glVertex3f(0.0, 0.0, 1.0)
    glEnd()
    glFlush()


def draw_cam(
    pos: np.ndarray,
    rot_mat: np.ndarray,
    radius: float,
    side_num=20,
    edge_only=True,
    color: Tuple[float, float, float] = None,
):
    """
    Draw a reference of a camera position based on a cone
    :param pos: position of the camera (3,)
    :param rot_mat: rotation matrix of the camera (3, 3)
    :param radius: cone radius
    :param side_num: number of sides to represent the cone
    :param edge_only: if True, only draw the polygon edges
    :param color: color of the cone
    """
    # prepare data
    color = (1.0, 1.0, 1.0) if color is None else color
    glColor3f(*color)
    if edge_only:
        glBegin(GL_LINE_LOOP)
    else:
        glBegin(GL_POLYGON)
    vertices = []

    # build transformation matrix
    T = np.eye(4)
    T[:3, :3] = rot_mat
    T[:3, -1] = pos

    # build circle vertices and connect them
    for idx in range(0, side_num):
        angle = idx * 2.0 * np.pi / side_num
        vertex = np.array([np.cos(angle) * radius, np.sin(angle) * radius, 0.5])
        vertex = (T @ np.append(vertex, 1.0))[:3]
        vertices.append(vertex)
        glVertex3f(*vertex)
    glEnd()

    # connect circle vertices with camera center
    glBegin(GL_LINES)
    for vertex in vertices:
        glVertex3f(*pos)
        glVertex3f(*vertex)
    glEnd()

    # draw a small coordinate system for reference
    draw_coordinates(rot_mat, pos, scale=0.2)
    glFlush()


def draw_rectangle(x: int, y: int, w: int, h: int, color: list = None):
    """
    Draws a rectangle onto the screen
    :param x: x position of the rectangle
    :param y: y position of the rectangle
    :param w: width of the rectangle
    :param h: height of the rectangle
    :param color: color of the rectangle; 3 or 4 values (RGB or RGBA)
    :return:
    """
    # prepare color
    if color is None:
        color = [1.0, 1.0, 1.0, 1.0]
    elif len(color) == 3:
        color.append(1.0)
    glColor4f(*color)

    # draw rectangle
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x, y)
    glTexCoord2f(0, 1)
    glVertex2f(x, y + h)
    glTexCoord2f(1, 1)
    glVertex2f(x + w, y + h)
    glTexCoord2f(1, 0)
    glVertex2f(x + w, y)
    glEnd()


def draw_texture(x: int, y: int, w: int, h: int, texture: Texture):
    """
    Draws a texture onto the screen
    :param x: x position of the texture rectangle
    :param y: y position of the texture rectangle
    :param w: width of the texture rectangle
    :param h: height of the texture rectangle
    :param texture: texture to project onto the rectangle
    :return:
    """
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture.location)
    glBindSampler(0, texture.sampler_id)

    draw_rectangle(x, y, w, h)

    glBindTexture(GL_TEXTURE_2D, 0)
    glBindSampler(0, 0)
    glDisable(GL_TEXTURE_2D)
