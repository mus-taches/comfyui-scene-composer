import numpy as np

from ...components.blackboard import Blackboard

from ...utils.config import get_project_name
from ._inputs import build_inputs, apply_input_values
from ._variables import apply_variables
from ._tags import choose_random_tags, stringify_tags


class NodeFactory:
    """
    Create nodes dynamically according to config files.
    """

    def __init__(self):
        self.name = self.__class__.__name__.lower()
        self.data = Blackboard().config[self.name]
        self.variables = Blackboard().variables

    @classmethod
    def INPUT_TYPES(cls):
        instance = cls()
        inputs = build_inputs(instance)
        inputs["required"]["seed"] = ("INT", {
            "default": 0,
            "min": 0,
            "max": 0xffffffffffffffff
        })
        return inputs

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build_prompt"
    PROJECT_NAME = get_project_name()
    CATEGORY = f"{PROJECT_NAME}/⭐️ My Nodes"

    def build_prompt(self, **args):
        """
        Build the prompt according to the node inputs the user selected.
        Concatenate the tags and return the prompt.
        """
        rng = np.random.default_rng(args["seed"])

        # Apply node's input values
        tags_from_data = self.data.get("tags", {})
        tags_from_inputs = apply_input_values(data=tags_from_data, inputs=args)

        # Add variables to the blackboard
        variables = self.data.get("variables", {})
        for key, value in variables.items():
            self.variables.update({key: value})

        # Select tags randomly and update the variables
        tags = {}
        for key, value in tags_from_inputs.items():
            tags[key] = choose_random_tags(rng, value)
            apply_variables(rng, tags[key], self.variables)
            self.variables.update({key: tags[key]})

        # Apply variables to the tags
        tags = apply_variables(rng, tags, self.variables)
        prompt = stringify_tags(tags.values(), ", ")
        self.variables.update({self.name: prompt})

        return (prompt,)

    @classmethod
    def create_node(cls, node_id, node_name=None):
        "Create a new node with ID and name"
        return type(node_id, (cls,), {
            "id": node_id,
            "name": node_name or node_id.capitalize()
        })

    __all__ = ["NodeFactory"]
