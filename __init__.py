from .py.scene import Scene
from .py.components.composition import Composition
from .py.components.action import Action
from .py.components.character.character import Character
from .py.components.clothes import Clothes
from .py.components.environment import Environment

NODE_CLASS_MAPPINGS = {
    "🎞️ Scene": Scene,
    "📹 Composition": Composition,
    "🎬 Action": Action,
    "👤 Character": Character,
    "👕 Clothes": Clothes,
    "⛅️ Environment": Environment,
}

WEB_DIRECTORY = "js"

__all__ = ['NODE_CLASS_MAPPINGS', "WEB_DIRECTORY"]
