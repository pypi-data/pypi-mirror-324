#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Standalone functions for texture image operations
@File      : textures.py
@Project   : pygletPlayground
@Time      : 07.12.22 19:08
@Author    : flowmeadow
"""
import ctypes
import ctypes as ct
import os
import warnings
from dataclasses import dataclass
from typing import Tuple, Optional, Union, List

import numpy as np
import PIL.Image
from pyglet.gl import *

TEXTURE_FORMATS = {"RGB": GL_RGB, "L": GL_DEPTH_COMPONENT}


@dataclass
class ImageData:
    """
    Dataclass for images that contains a ctypes byte array, the size of the image in pixels and the Pillow image format.
    """

    c_data: ctypes.Array
    img_size: Tuple[int, int]
    img_mode: str


def img_file_to_byte_array(path: str, save: bool = False) -> ImageData:
    """
    Converts an image file to a ctypes array and returns it as an ImageData object.
    :param path: path to the image file (supported file types: PNG, JPEG, PPM, GIF, TIFF, and BMP)
    :param save: If True, the ctypes array is saved in a custom format (IBA) in the same directory. This format can be
    loaded much faster which is useful for a high amount of textures or high resolution images. Be sure to have enough
    disk space, as those files can get quite big.
    :return: ImageData object
    """
    # open image and convert it to a numpy array
    img = PIL.Image.open(path)  # .jpg, .bmp, etc. also work
    img_data = np.array(list(img.getdata()), np.int8)

    img_size, img_mode = img.size, img.mode
    data_type = np.ubyte  # default

    # transform array and get data length
    data = np.array(img_data, dtype=data_type).flatten()
    data_count = data.shape[0]

    # convert to ctypes array
    c_data = (ct.c_ubyte * data_count)()
    c_data[:] = data

    if save:
        # save ctypes array as a binary file
        directory, base = os.path.split(path)
        file_name, _ = os.path.splitext(base)
        out_path = os.path.join(directory, f"{file_name}.iba")
        with open(out_path, "wb") as f:
            f.write(data)
        # save image size and mode as metadata
        os.setxattr(out_path, "user.img_width", bytearray(str(img_size[0]), "utf-8"))
        os.setxattr(out_path, "user.img_height", bytearray(str(img_size[1]), "utf-8"))
        os.setxattr(out_path, "user.img_mode", bytearray(str(img_mode), "utf-8"))

    return ImageData(c_data, img_size, img_mode)


def load_image_byte_array(texture: Union[np.ndarray, str]) -> ImageData:
    """
    Given a file path, image data is loaded and returned as an ImageData object
    :param texture: Numpy array or file path to the image object
    :return: ImageData object
    """
    if isinstance(texture, np.ndarray):
        # transform array and get data length
        arr = np.uint8(texture * 255)
        img_size = arr.shape[:2]
        if len(arr.shape) == 2:
            img_mode = "L"
        elif len(arr.shape) == 3:
            img_mode = "RGB"
        else:
            raise NotImplementedError()

        # convert to ctypes array
        arr = arr.flatten()
        data_count = arr.shape[0]
        c_data = (ct.c_ubyte * data_count)()
        c_data[:] = arr

        img_data = ImageData(c_data, img_size, img_mode)

    elif isinstance(texture, str):
        _, extension = os.path.splitext(texture)

        # load from image file
        if extension in [".jpg", ".jpeg", ".png", ".bmp"]:
            img_data = img_file_to_byte_array(texture)
        # load from image byte array file (custom)
        elif extension in [".iba"]:
            with open(texture, "rb") as f:
                c_data = f.read()
            w = os.getxattr(texture, "user.img_width")
            h = os.getxattr(texture, "user.img_height")
            img_mode = os.getxattr(texture, "user.img_mode").decode("utf-8")
            img_size = (int(w), int(h))
            img_data = ImageData(c_data, img_size, img_mode)
        else:
            raise NotImplementedError()
    else:
        raise NotImplementedError()
    return img_data


def load_texture(
    texture: Union[np.ndarray, str], location: Optional[GLuint] = None, texture_parameters: List[Tuple[int, int]] = None
):
    """
    Given a file path, image data loaded and stored as a texture on the GPU
    :param texture: Numpy array or file path to the image object
    :param location: location of the texture
    :return: OpenGL location of the texture
    """
    img_data = load_image_byte_array(texture)
    c_data, img_size, img_mode = img_data.c_data, img_data.img_size, img_data.img_mode
    img_format = TEXTURE_FORMATS[img_mode]

    if location is None:
        location = GLuint()
    glEnable(GL_TEXTURE_2D)

    glGenTextures(1, location)
    glBindTexture(GL_TEXTURE_2D, location)

    defaults = {
        GL_TEXTURE_WRAP_S: GL_REPEAT,
        GL_TEXTURE_WRAP_T: GL_REPEAT,
        GL_TEXTURE_MIN_FILTER: GL_LINEAR_MIPMAP_LINEAR,
        GL_TEXTURE_MAG_FILTER: GL_LINEAR,
    }
    if isinstance(texture_parameters, list):
        for (new_key, new_val) in texture_parameters:
            defaults[new_key] = new_val
    for key, val in defaults.items():
        glTexParameteri(GL_TEXTURE_2D, key, val)

    # glSamplerParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, img_format, img_size[0], img_size[1], 0, img_format, GL_UNSIGNED_BYTE, c_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    glDisable(GL_TEXTURE_2D)

    return location


def wrap_texture(vertices: np.ndarray, method: str = "cylinder") -> np.ndarray:
    """
    Computes texture coordinates for an array of vertices
    :param vertices: vertex array [n, 3]
    :param method: wrapping method
    :return: texture coordinate array [n, 2]
    """
    min_vec = np.min(vertices, axis=0)
    max_vec = np.max(vertices, axis=0)
    mid_vec = (max_vec + min_vec) / 2

    if method == "cylinder":
        # cylindrical wrapping method
        vertices_mid = vertices[:, :2] - mid_vec[:2]
        x, y = vertices_mid[:, 0], vertices_mid[:, 1]
        r = (1.0 + -np.arctan2(x, y) / np.pi) / 2

        z_min, z_max = min_vec[2], max_vec[2]
        z = 1.0 - (vertices[:, 2] - z_min) / (z_max - z_min)
        return np.array([r, z]).T
    else:
        raise NotImplementedError()


def generate_height_map(grid_size=(100, 100), seed=0, num_iter=100, counter=0, smoothness=0.5, experimental_mode=False):
    max_size = 100
    max_iter = 100

    if max(grid_size) > max_size and not experimental_mode:
        grid_size = [min(g, max_size) for g in grid_size]
        warnings.warn(
            f"\nGrid size of more than {max_size} is not recommended as the computation increases exponentially."
            f"\nIf you want to compute with higher grid sizes, set the 'experimental_mode' flag. "
        )
    if num_iter > max_iter and not experimental_mode:
        num_iter = max_iter
        warnings.warn(
            f"\nMore than {max_iter} iterations is not recommended as the computation increases exponentially."
            f"\nIf you want to compute with more iterations, set the 'experimental_mode' flag. "
        )
    np.random.seed(seed)

    x_arr, y_arr = np.arange(grid_size[0]) / grid_size[0], np.arange(grid_size[1]) / grid_size[1]
    grid_pts = np.array(np.meshgrid(y_arr, x_arr)).T.reshape(-1, 2)
    height_map = np.zeros(grid_size)
    rand_pts = np.random.random((num_iter, 4))

    rand_pts[:, 0] += 0.01 * np.sin(counter)
    rand_pts[:, 1] += 0.01 * np.cos(counter)

    p_1_arr, p_2_arr = rand_pts[:, :2], rand_pts[:, 2:]
    for p_1, p_2 in zip(p_1_arr, p_2_arr):
        heights = np.cross(p_2 - p_1, grid_pts - p_1) / np.linalg.norm(p_2 - p_1)
        heights = np.tanh(heights * 2**(smoothness * 8))
        height_map += heights.reshape(grid_size)
    height_map = (height_map - np.min(height_map)) / (np.max(height_map) - np.min(height_map))
    return height_map


class ColorMap:
    def __init__(self):
        self.key_points = []
        self.r_arr = []
        self.g_arr = []
        self.b_arr = []
        self.cmap_arr = None

    def add(self, value, color):
        self.key_points.append(value)
        self.r_arr.append(color[0])
        self.g_arr.append(color[1])
        self.b_arr.append(color[2])

        self.cmap_arr = np.concatenate([[self.key_points], [self.r_arr], [self.g_arr], [self.b_arr]], axis=0).T

    def arr2img(self, arr):
        img_arr = np.zeros((*arr.shape, 3))
        img_arr[:, :, 0] = np.interp(arr, self.cmap_arr[:, 0], self.cmap_arr[:, 1])
        img_arr[:, :, 1] = np.interp(arr, self.cmap_arr[:, 0], self.cmap_arr[:, 2])
        img_arr[:, :, 2] = np.interp(arr, self.cmap_arr[:, 0], self.cmap_arr[:, 3])
        img_arr[:, :, 2] = np.interp(arr, self.cmap_arr[:, 0], self.cmap_arr[:, 3])

        return img_arr


class ClassicColorMap(ColorMap):
    def __init__(self):
        super().__init__()
        super().add(0.00, [0.0, 0.0, 1.0])
        super().add(0.25, [0.0, 1.0, 1.0])
        super().add(0.50, [0.0, 1.0, 0.0])
        super().add(0.75, [1.0, 1.0, 0.0])
        super().add(1.00, [1.0, 0.0, 0.0])

    def add(self, *args):
        warnings.warn("Default colormaps don't have an add function")
        pass
