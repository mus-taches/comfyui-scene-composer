import numpy as np
from ..utils.config import get_project_name, load_config
from .node_factory._variables import apply_variables
from ..components.blackboard import Blackboard


class Composer:
    """
    A ComfyUI node to compose prompt with variables.
    Inputs: string with {variables}
    Output: prompt composed with variables
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("prompt", "variables", )
    FUNCTION = "build_prompt"
    PROJECT_NAME = get_project_name()
    CATEGORY = f"{PROJECT_NAME}/🛠️ Utils"

    def build_prompt(self, **args):
        """
        Transform tags, subtags and variables as reusable {variables}
        Return the prompt with the variables replaced
        """
        rng = np.random.default_rng(args["seed"])

        # Extract variables
        variables = args.get("variables")

        if not variables:
            variables = load_config("variables", with_filename=False)

        Blackboard().variables = variables

        prompt = args["prompt"]
        prompt = apply_variables(rng, prompt, variables)

        return (prompt[0],)
