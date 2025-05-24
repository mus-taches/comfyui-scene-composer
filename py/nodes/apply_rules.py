import fnmatch
import dpath
import numpy as np

from ..utils.config import get_project_name
from .node_factory._tags import choose_random_tags, stringify_tags
from .node_factory._variables import apply_variables
from ..components.blackboard import Blackboard


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
        self.config = Blackboard().config.copy()
        self.rules = Blackboard().rules.copy()

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
            "optional": {
                "variables": ("STRING", {"forceInput": True})
            }
        }

    def apply_rules(self, prompt, ruleset, seed, variables=None):
        """
        Apply the rules defined in config file.
        Add and remove tags in the prompt
        according to others tags in the same prompt
        """
        rng = np.random.default_rng(seed)

        # Put prompt in a tag list
        tags = [tag.strip() for tag in prompt.replace(
            "\n", ", ").split(",") if tag.strip()]

        # Merge rule config files
        if ruleset == "all":
            rules = [rule for rule_set in self.rules.values()
                     for rule in rule_set]
        else:
            rules = self.rules.get(ruleset, [])

        # Apply the rules
        for rule in rules:
            triggers = rule["triggers"]
            logic = rule.get("logic", "OR")
            actions = rule["actions"]
            p = rule.get("probability", 1)

            if rng.random() > p:
                continue

            # If any triggering tag occurs in the prompt,
            # run all the defined actions
            if logic == "OR":
                for trigger in triggers:
                    if any(fnmatch.fnmatch(tag, trigger) for tag in tags):
                        tags = run_actions(rng, actions, tags, self.config)
                        continue

            elif logic == "AND":
                if all(any(fnmatch.fnmatch(tag, trigger) for tag in tags) for trigger in triggers):
                    tags = run_actions(rng, actions, tags, self.config)

        if variables:
            tags = apply_variables(rng, tags, variables)

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

            # Add tags at the end of the prompt
            case "add":
                value = choose_random_tags(rng, filtering_tags)
                process_tags.append(value)

            # Remove any tag that matches the value
            case "remove":
                process_tags = [
                    tag for tag in process_tags
                    if not any(fnmatch.fnmatch(tag, v)
                               for v in filtering_tags)]

            # In any tag that matches the filter, replace the value with the new one
            case "replace":
                filter = process_action_value(
                    action.get("filter", ["*"]), config)

                new_value = action.get("new_value", [])
                new_value = choose_random_tags(rng, new_value)

                # Handle string value
                if isinstance(value, str) and value != "*":
                    value = [value]

                # Handle list value
                if isinstance(value, list) and len(value) > 0:
                    for v in value:
                        process_tags = [
                            tag.replace(v, new_value)
                            if any(fnmatch.fnmatch(tag, pattern) for pattern in filter)
                            else tag
                            for tag in process_tags
                        ]

                # For any other case, replace the whole tag
                else:
                    process_tags = [new_value if any(fnmatch.fnmatch(
                        tag, pattern) for pattern in filter) else tag for tag in process_tags]

    return process_tags


def process_action_value(value, config):
    """
    Process the action's value.
    Return selected tags randomly or according to a given path
    """

    tags = []

    if isinstance(value, dict):
        return value

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
    is_path = isinstance(string, str) and ("/" in string)
    return is_path
