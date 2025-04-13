from ..utils.config import get_project_name


class MergeStrings:
    """
    A ComfyUI node to merge string.
    Inputs: strings (stacked)
    Output: merged string
    Check merge_strings.js for the frontend implementation.
    """
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "merge_strings"

    PROJECT_NAME = get_project_name()
    CATEGORY = f"{PROJECT_NAME}/🛠️ Utils"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "separator": ("STRING", {"default": ", "})
            },
            "optional": {}
        }

    def merge_strings(self, separator, **kwargs):
        value = separator.join(
            v for v in kwargs.values()
            if isinstance(v, str)
        )
        return (value,)
