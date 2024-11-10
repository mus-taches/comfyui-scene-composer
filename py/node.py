import numpy as np
import toml
from server import PromptServer

from .constants import ROOT_DIR


class Node:
    """ComfyUI Node parent class
    Will build and return a prompt according to other sub-components.
    """

    def __init__(self, seed=0, data_file=""):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.data = self.load_data(data_file)

    @classmethod
    def INPUT_TYPES(cls):
        """ComfyUI node's inputs"""
        inputs = {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                })
            },
            "optional": {},
            "hidden": {"ident": "UNIQUE_ID"}
        }
        return inputs

    RETURN_TYPES = ("STRING",)
    FUNCTION = "build_prompt"
    CATEGORY = "🎞️ Scene Composer"

    def build_prompt(self, seed):
        self.rng = np.random.default_rng(seed)
        pass

    def select_tags(self, tags, p=1, n=1, selected="random", recursive=True):
        """Return n tags from a string, list or dict
        p: probability of selecting the tags
        n: number of tags to select
        selected: fallback tag to select if not random
        recursive: go deeper randomly to select last children tags"""

        if selected != "random":
            return selected

        if isinstance(tags, dict):

            p = tags.get("probability", p)
            n = tags.get("repeat", n)

            if self.rng.random() > p:
                return ""

            # If n is a list, choose a random number between the 2 first values
            if isinstance(n, list):
                min_n = n[0]
                max_n = min(n[1], len(tags))
                n = self.rng.integers(int(min_n), int(max_n))

            # Handle "list" and "tags" special keys
            if "list" in tags:
                selected_from_list = self.select_tags(tags["list"], p, n)
                selected_from_list = selected_from_list.split(", ")
                tag_list = []
                for item in selected_from_list:
                    tag_list.append(self.select_tags(tags[item]))

                tags = tag_list

            elif "tags" in tags:
                tags = tags.get("tags", [])

            # Handle recursive tags
            else:
                first_level_keys = list(tags.keys())
                chosen_key = self.rng.choice(first_level_keys)
                chosen_value = tags[chosen_key]

                if isinstance(chosen_value, (list, dict)):
                    tags = self.select_tags(chosen_value, p, n)

                if not recursive:
                    tags = first_level_keys

        if isinstance(tags, list):
            tag_names, weights = self.parse_tag_distribution(tags)

            # If n is a list, choose a random number between the 2 first values
            if isinstance(n, list):
                min_n = n[0]
                max_n = min(n[1], len(tags))
                n = self.rng.integers(int(min_n), int(max_n))

            selected_tags = self.rng.choice(
                tag_names,
                size=n,
                replace=False,
                p=weights
            )
            tags = self.stringify_tags(selected_tags)

        return tags

    @staticmethod
    def parse_tag_distribution(tags):
        """Choose tags randomly according to defined weights
        If none are defined, tag weight is 1
        Example: "foo[1.5], bar[0.5]" -> 75% chance of foo, 25% chance of bar
        """
        tag_names = []
        weights = []
        for tag in tags:
            if '[' in tag and ']' in tag:
                tag_name, weight = tag.split('[')
                weight = weight.rstrip(']')
                tag_names.append(tag_name)
                weights.append(float(weight))
            else:
                tag_names.append(tag)
                weights.append(1)
        probabilities = np.array(weights) / sum(weights)
        return tag_names, probabilities

    @staticmethod
    def load_data(filename):
        """Load data from a TOML file"""
        path = f"{ROOT_DIR}/config/{filename}"
        try:
            with open(path) as file:
                data = toml.load(file)
        except Exception:
            data = {}
        return data

    @staticmethod
    def build_inputs_list(data):
        """Build a list with a random option"""

        inputs_list = ["random"]

        if "tags" in data:
            data = data["tags"]

        for tag in data:
            if '[' in tag and ']' in tag:
                tag = tag.split('[')[0]
            inputs_list.append(tag)

        return inputs_list

    @staticmethod
    def stringify_tags(tags):
        """Return a string from a list of tags
        Remove extra commas and spaces"""

        # Convert numpy array to list if necessary
        if isinstance(tags, np.ndarray):
            tags = tags.tolist()

        # Convert all tags to strings and join them with commas
        tags = ', '.join(map(str, tags))

        # Remove extra commas and spaces
        tags = ', '.join(filter(None, map(str.strip, tags.split(','))))
        return tags

    def __str__(self, **kwargs):
        return self.build_prompt(**kwargs)[0]

    # Generic function to send messages to Javascript
    @staticmethod
    def comfy_message(route: str, ident: str, data: dict) -> None:
        data['id'] = ident
        PromptServer.instance.send_sync(route, data)
