import os

from setuptools import find_packages, setup

# os.system("pip freeze > requirements.txt")
# REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
# print(REQUIREMENTS)
setup(
    name="glpg",
    version="1.0.0",
    license="MIT",
    packages=find_packages(include=["glpg", "glpg.*"]),
    install_requires=[
        "attrs==25.1.0",
        "numpy==2.2.2",
        "pillow==11.1.0",
        "pyglet==1.5.27",
        "PySide6==6.8.2",
        "PySide6_Addons==6.8.2",
        "PySide6_Essentials==6.8.2",
        "shiboken6==6.8.2",
        "typing_extensions==4.12.2",
    ],
    include_package_data=True,
    description="pyglet OpenGL playground",
    author="Florian Wiese",
    author_email="florian-wiese93@outlook.de",
    url="https://github.com/flowmeadow/pygletPlayground",
    download_url="https://github.com/flowmeadow/pygletPlayground.git",
    keywords=["pyglet", "OpenGL"],
)
