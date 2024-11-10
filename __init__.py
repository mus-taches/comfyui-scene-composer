from .py.scene import Scene
from .py.components.composition import Composition
from .py.components.action import Action
from .py.components.character.character import Character
from .py.components.clothes import Clothes
from .py.components.environment import Environment
import os

# Dynamic widget lists with CozySpoke
cozy_spoke_path = os.path.join(
    os.path.dirname(__file__), 'py', 'cozy_spoke.py')
with open(cozy_spoke_path) as f:
    exec(f.read())

# Mappings
NODE_CLASS_MAPPINGS = {
    "Scene": Scene,
    "Composition": Composition,
    "Action": Action,
    "Character": Character,
    "Clothes": Clothes,
    "Environment": Environment,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Scene": "🎞️ Scene",
    "Composition": "📹 Composition",
    "Action": "🎬 Action",
    "Character": "👤 Character",
    "Clothes": "👕 Clothes",
    "Environment": "⛅️ Environment",
}

WEB_DIRECTORY = "js"

__all__ = ['NODE_CLASS_MAPPINGS',
           "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
