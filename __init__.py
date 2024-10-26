from .src.scene import Scene
from .src.components.composition import Composition
from .src.components.action import Action
from .src.components.character.character import Character
from .src.components.clothes import Clothes
from .src.components.environment import Environment

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
