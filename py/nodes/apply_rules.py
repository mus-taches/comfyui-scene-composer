import fnmatch
import dpath
import numpy as np

from ..utils.config import get_project_name, load_config
from .node_factory._tags import select_tags, stringify_tags


class ApplyRules:
    """
    A ComfyUI node to apply rules to a string.
    Input: string
    Output: filtered string
    """
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "apply_rules"
    PROJECT_NAME = get_project_name()
    CATEGORY = f"{PROJECT_NAME}/🛠️ Utils"

    def __init__(self):
        self.config = load_config()
        self.rules = load_config("rules")

    @classmethod
    def INPUT_TYPES(cls):
        instance = cls()
        rules = list(instance.rules.keys())

        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "ruleset": (["all", *rules],),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                }),
            },
            "optional": {}
        }

    def apply_rules(self, prompt, ruleset, seed):
        """
        Apply the rules defined in config file.
        Add and remove tags in the prompt
        according to others tags in the same prompt
        """
        rng = np.random.default_rng(seed)
        tags = [tag.strip() for tag in prompt.replace(
            "\n", ", ").split(", ") if tag.strip()]
        rules = {key: value.copy() for key, value in self.rules.items()}

        # Merge all the rule together
        if ruleset == "all":
            merged_rules = {}
            for r_name, r_list in rules.items():
                for rule in r_list:
                    for key, value in rule.items():
                        if key not in merged_rules:
                            merged_rules[key] = []
                        if isinstance(value, list):
                            merged_rules[key].extend(value)
                        else:
                            merged_rules[key].append(value)
            rules["all"] = [merged_rules]

        # Apply the rules
        for rule in rules[ruleset]:
            triggers = rule["triggers"]
            actions = rule["actions"]
            p = rule.get("probability", 1)

            if rng.random() > p:
                continue

            # If any triggering tag occurs in the prompt,
            # run all the defined actions
            for trigger in triggers:
                if fnmatch.fnmatch(prompt, trigger):
                    tags = run_actions(rng, actions, tags, self.config)
                    break

        tags = stringify_tags(tags, separator=", ")
        return (tags,)


def run_actions(rng, actions, tags, config):
    """
    Run actions from the rule.
    Add or remove tags with filtering tags
    """

    process_tags = tags.copy()

    for action in actions:

        type = action.get("type", "add")
        value = action.get("value", [])
        p = action.get("probability", 1)

        if rng.random() > p:
            continue

        filtering_tags = process_action_value(value, config)

        match type:

            case "add":
                value = select_tags(rng, filtering_tags)
                process_tags.append(value)

            case "remove":

                # filter: remove tags that match any "remove" value
                process_tags = [tag for tag in process_tags
                                if not any(
                                    fnmatch.fnmatch(tag, f"*{v}*")
                                    for v in filtering_tags
                                )]

    return process_tags


def process_action_value(value, config):
    """
    Process the action's value.
    Return selected tags randomly or according to a given path
    """

    tags = []

    if isinstance(value, str):
        value = [value]

    # If the value is a path,
    # take all the tags from this path
    for v in value:
        if is_path(v):
            for k, i in dpath.search(config, v,
                                     yielded=True, dirs=False):
                if isinstance(i, str):
                    tags.append(i)
        else:
            tags.append(v)

    return tags


def is_path(string):
    "Check if the value is a glob path"
    is_path = isinstance(string, str) and ("/" in string or "*" in string)
    return is_path
