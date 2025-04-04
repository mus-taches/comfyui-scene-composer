import numpy as np
import fnmatch
from .node_factory._tags import stringify_tags


class CleanupPrompt:
    """
    A ComfyUI node to clean up your prompt.
    Sort tags and remove duplications
    Inputs: string
    Output: string
    """
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "cleanup_prompt"
    CATEGORY = "⚙️ Prompt Factory/🛠️ Utils"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "cleanup": ("BOOLEAN", {"default": True}),
                "sort": (["none", "asc", "desc", "random"]),
                "custom_sort": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                })
            },
            "optional": {}
        }

    def cleanup_prompt(self, prompt, cleanup, sort, custom_sort, seed):

        tags = prompt.split(", ")

        if cleanup is True:
            tags = self.remove_duplicates(tags)

        match sort:

            case "asc": tags = sorted(tags)
            case "desc": tags = sorted(tags, reverse=True)
            case "random":
                np.random.seed(seed)
                np.random.shuffle(tags)

        if custom_sort != "":
            custom_sort = custom_sort.split(", ")
            custom_order_dict = {}
            for i, pattern in enumerate(custom_sort):
                for tag in tags:
                    if fnmatch.fnmatch(tag, pattern):
                        custom_order_dict[tag] = i

            tags = sorted(tags, key=lambda x:
                          custom_order_dict.get(x, len(custom_order_dict)))

        prompt = stringify_tags(tags.values(), ", ")
        return (prompt,)

    def remove_duplicates(tags):
        seen = set()
        unique_tags = []
        for tag in tags:
            if tag not in seen:
                unique_tags.append(tag)
                seen.add(tag)
        return unique_tags
