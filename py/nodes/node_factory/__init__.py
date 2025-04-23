import numpy as np
import json

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
        self.variables = {}

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
    PROJECT_NAME = get_project_name()
    CATEGORY = f"{PROJECT_NAME}/⭐️ My Nodes"

    def build_prompt(self, **args):
        """
        Build the prompt according to the node inputs the user selected.
        Concatenate the tags and return the prompt.
        """
        rng = np.random.default_rng(args["seed"])
        settings = self.data.get("settings", {})

        # Apply node's input values
        tags_from_data = self.data.get("tags", {})
        tags_from_inputs = apply_input_values(data=tags_from_data, inputs=args)

        # Process variables
        global_variables = Blackboard().variables.copy()
        received_variables = args.get("variables", {})

        if isinstance(received_variables, str):
            if received_variables == "":
                received_variables = {}
            else:
                received_variables = json.loads(received_variables)

        local_variables = self.data.get("variables", {})
        local_variables = apply_input_values(data=local_variables, inputs=args)

        self.variables = {
            **global_variables,
            **received_variables,
            **local_variables
        }

        share_variables = settings.get("share_variables", True)
        output_variables = settings.get("output_variables", False)
        tags = {}

        for key, value in self.variables.items():

            # Share this variable with next nodes
            share_variable = share_variables
            if isinstance(value, dict):
                share_variable = value.get("share", share_variables)
            if share_variable:
                self.variables.update({key: value})

            # Add this variable to the prompt
            output_variable = output_variables
            if isinstance(value, dict):
                output_variable = value.get("output", output_variables)
            if output_variable:
                tags[key] = choose_random_tags(rng, value)

        # Select tags randomly and update the variables
        rng_state = rng.bit_generator.state
        for key, value in tags_from_inputs.items():
            tags[key] = choose_random_tags(rng, value)
            apply_variables(rng, tags[key], self.variables)
            self.variables.update({key: tags[key]})
        rng.bit_generator.state = rng_state

        # Apply variables to the tags
        tags = apply_variables(rng, tags, self.variables)
        prompt = stringify_tags(tags.values(), ", ")

        # Handle output
        output = self.data.get("output", True)
        output = args.get("output", output)

        match output:
            case str():
                output = apply_variables(rng, output, self.variables)
                output = stringify_tags(output, ", ")
            case True:
                output = prompt
            case False:
                output = ""

        self.variables.update({self.name: output})
        return (output, self.variables,)

    @classmethod
    def create_node(cls, node_id, node_name=None):
        "Create a new node with ID and name"
        return type(node_id, (cls,), {
            "id": node_id,
            "name": node_name or node_id.capitalize()
        })

    __all__ = ["NodeFactory"]
