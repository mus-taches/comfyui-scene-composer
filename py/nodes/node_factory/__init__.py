import numpy as np
import json

from ...utils.config import load_config
from ._inputs import build_inputs, apply_input_values
from ._variables import apply_variables
from ._tags import select_tags, stringify_tags


class NodeFactory:

    def __init__(self):
        config = load_config()
        self.name = self.__class__.__name__.lower()
        self.data = config[self.name]

    @classmethod
    def INPUT_TYPES(cls):
        instance = cls()
        inputs = build_inputs(instance)
        inputs["required"]["seed"] = ("INT", {
            "default": 0,
            "min": 0,
            "max": 0xffffffffffffffff
        })
        inputs["optional"]["variables"] = ("STRING", {"defaultInput": True})
        return inputs

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("prompt", "variables",)
    FUNCTION = "build_prompt"
    CATEGORY = "⚙️ Prompt Factory/⭐️ My Nodes"

    def build_prompt(self, **args):
        """
        Build the prompt according to the node inputs
        Concatenate the tags and return the prompt
        """
        rng = np.random.default_rng(args["seed"])

        # Build inputs
        tags = self.data.get("tags", {})
        inputs_tags = apply_input_values(tags, args)

        variables = self.data.get("variables", {})
        local_variables = apply_input_values(variables, args)

        # Select tags
        tags = {}
        for key, value in inputs_tags.items():
            tags[key] = select_tags(rng, value)

        # Replace tags with corresponding variables
        global_variables = load_config("variables", with_filename=False)
        optional_variables = args.get("variables", {})

        if isinstance(optional_variables, str):
            optional_variables = json.loads(optional_variables)

        variables = {
            **global_variables,
            **local_variables,
            **optional_variables
        }

        tags = apply_variables(rng, tags, variables)
        variables = {**variables, **tags}

        # Build and clean-up final prompt
        prompt = stringify_tags(tags.values(), ", ")
        variables = {**variables, self.__class__.__name__.lower(): prompt}

        return (prompt, variables,)

    @classmethod
    def create_node(cls, node_id, node_name=None):
        "Create a new node with ID and name"
        return type(node_id, (cls,), {
            "id": node_id,
            "name": node_name or node_id.capitalize()
        })

    __all__ = ["NodeFactory"]
