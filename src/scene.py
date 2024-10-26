from .node import Node
from .components.composition import Composition
# from .components.action.action import Action
from .components.action import Action
from .components.character.character import Character
from .components.clothes import Clothes
from .components.environment import Environment


class Scene(Node):

    def __init__(self, seed=0, data_file=""):
        super().__init__(seed)

        self.components = {
            "composition": {
                "default": Composition(),
                "prefix": '',
                "protagonists": '1girl, solo',
                "camera_framing": 'random',
                "camera_angle": 'random'
            },
            "action": {
                "default": Action(),
                "nsfw": True,
                "position": "random",
                "gesture": "random",
                "act_type": "random",
                "act": "random"
            },
            "character": {
                "default": Character(),
            },
            "clothes": {
                "default": Clothes(),
            },
            "environment": {
                "default": Environment(),
            }
        }

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        seed = inputs["required"]["seed"]

        components = cls().components

        inputs["required"] = {
            "seed": seed
        }

        # Add the components as optional inputs
        optional_components = {
            key: ("STRING", {
                "default": "",
                "forceInput": True
            })
            for key in components.keys()
        }
        inputs["optional"] = optional_components

        return inputs

    def build_prompt(self, seed, **kwargs):
        components = self.components
        prompt = []

        # Build each component's prompt
        # If the component is in the kwargs, use it
        # Otherwise, use a default component
        for component_name, component_data in components.items():

            tags = ""

            if "default" in component_data:
                default = component_data["default"]
                args = component_data.copy()
                args.pop("default")
                tags = default.build_prompt(seed, **args)[0]

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
