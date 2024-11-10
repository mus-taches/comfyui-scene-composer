from .node import Node
from .components.composition import Composition
from .components.action import Action
from .components.character.character import Character
from .components.clothes import Clothes
from .components.environment import Environment


class Scene(Node):

    def __init__(self, seed=0, data_file=""):
        super().__init__(seed)

        self.components = {
            "composition": {
                "default": None,
                "prefix": '',
                "protagonists": '1girl, solo',
                "camera_framing": 'random',
                "camera_angle": 'random',
            },
            "action": {
                "default": None,
                "nsfw": False,
                "position": "random",
                "gesture": "random",
                "act_type": "random",
                "act": "random",
                "cum": False
            },
            "character": {
                "default": None,
            },
            "clothes": {
                "default": None,
            },
            "environment": {
                "default": None,
            }
        }

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        seed = inputs["required"]["seed"]

        components = cls().components

        inputs["required"] = {"seed": seed}

        # Add the components as optional inputs
        optional_components = {
            key: ("STRING", {
                "default": "",
                "forceInput": True
            })
            for key in components.keys()
        }

        inputs["optional"] = optional_components

        inputs["hidden"] = {"ident": "UNIQUE_ID"}

        return inputs

    def build_prompt(self, seed, ident, **kwargs):

        prompt = []
        components = self.components

        default_components = {
            "composition": Composition(seed),
            "action": Action(seed),
            "character": Character(seed),
            "clothes": Clothes(seed),
            "environment": Environment(seed)
        }

        # Build each component's prompt
        # If the component is in the kwargs, use it
        # Otherwise, use a default component
        for component_name, component_data in components.items():

            tags = ""

            if "default" in component_data:
                default = default_components[component_name]
                args = component_data.copy()
                args.pop("default")
                tags = default.build_prompt(seed, ident, **args)[0]

            if component_name in kwargs.keys():
                tags = kwargs[component_name] + ", "

            prompt.append(tags)

        # Clean up prompt
        # Seperate tags with commas and remove trailing commas
        prompt = self.stringify_tags(prompt)
        if prompt.startswith(", "):
            prompt = prompt[2:]
        if prompt.endswith(", "):
            prompt = prompt[:-2]

        return (prompt,)
