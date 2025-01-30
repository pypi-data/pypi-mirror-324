# Model 
# The Model module contains the structure, data, and tunable parameters for 
# a Parea architecture.
# We are heavily 
# https://www.reddit.com/r/learnmachinelearning/comments/x7dkva/understanding_keras_layer_chaining_syntax/
# https://t.ly/U4xp

from typing import Any


class Model(object):
    def __init__(self) -> None:
        pass
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print("Model Superclass")


class Cluster(Model):
    def __init__(self) -> None:
        self.tunable_parameters = [1,2,3]
        self.name = 

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise TypeError("Not callable")


class Fusion(Model):
        def __init__(self) -> None:
            super().__init__()

        def __call__(self, *args: Any, **kwds: Any) -> Any:
            super().__call__(*args, **kwds)
            return self

