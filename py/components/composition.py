from ..node import Node


class Composition(Node):

    def __init__(self, seed=0):
        super().__init__(seed, data_file="composition.toml")

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        seed = inputs["required"]["seed"]
        data = cls(seed).data

        prefix = data["prefix"]
        protagonists = cls().build_inputs_list(data["protagonists"])
        camera_framings = cls().build_inputs_list(data["camera"]["framings"])
        camera_angles = cls().build_inputs_list(data["camera"]["angles"])

        inputs["required"] = {
            "prefix": ("STRING", {"default": prefix, "multiline": True}),
            "protagonists": (protagonists,),
            "camera_framing": (camera_framings,),
            "camera_angle": (camera_angles,),
            "seed": inputs["required"]["seed"]
        }
        return inputs

    def build_prompt(self, seed, prefix, protagonists,
                     camera_framing, camera_angle):

        super().build_prompt(seed)

        components = {
            "prefix": {
                "tags": self.data["prefix"],
                "selected": prefix
            },
            "protagonists": {
                "tags": self.data["protagonists"],
                "selected": protagonists
            },
            "camera_framing": {
                "tags": self.data["camera"]["framings"],
                "selected": camera_framing
            },
            "camera_angle": {
                "tags": self.data["camera"]["angles"],
                "selected": camera_angle
            }
        }

        prompts = {}

        # Select tags for each component
        for name, params in components.items():
            prompt = self.select_tags(
                tags=params["tags"],
                selected=params["selected"]
            )
            prompts[name] = prompt

        # Protagonists enhancement
        match prompts["protagonists"]:
            case "1girl":
                prompts["protagonists"] = "1girl, solo"
            case "1girl, 1boy":
                prompts["protagonists"] = "1girl, 1boy, solo focus"

        # Build the prompt
        prompt = ", ".join(prompts.values())
        return (prompt,)
