# Pyrea: Multi-view hierarchical clustering with flexible ensemble structures
# Copyright (C) 2022 Marcus D. Bloice, Bastian Pfeifer
#
# Licenced under the terms of the MIT license.
#
# functional.py
# Contains implementation of the new Functional API. Inspired by Keras.

from typing import Any


class Cluster():
    def __init__(self) -> None:
        print("Initialised...")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print("Called...")


class Fusion():
    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass