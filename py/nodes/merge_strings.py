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
    CATEGORY = "⚙️ Prompt Factory/🛠️ Utils"

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
