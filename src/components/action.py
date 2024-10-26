from ..node import Node
from ..utils import is_true


class Action(Node):

    def __init__(self, seed=0):
        super().__init__(seed, data_file="actions.toml")

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        seed = inputs["required"]["seed"]
        data = cls().data

        positions = cls().build_inputs_list(data["sfw"]["positions"])
        gestures = cls().build_inputs_list(data["sfw"]["gestures"])
        act_types = cls().build_inputs_list(data["nsfw"]["acts"].keys())

        # Add act_type as prefix to each act in the list
        # (This will be filtered by the front-end, according to the act_type)
        acts = []
        for act_type in act_types:
            if act_type == "random":
                continue
            # If act_type is not in the list, select a random one
            if act_type not in data["nsfw"]["acts"]:
                act_type = cls().select_tags(
                    tags=data["nsfw"]["acts"],
                    selected=act_type,
                    recursive=False
                )
            for act in data["nsfw"]["acts"][act_type]:
                acts.extend([f"{act_type}_{act}"])
        acts = cls().build_inputs_list(acts)

        # Update the required inputs
        inputs["required"] = {
            "nsfw": ("BOOLEAN", {"default": False}),
            "position": (positions,),
            "gesture": (gestures,),
            "act_type": (act_types,),
            "act": (acts,),
            "seed": seed
        }

        return inputs

    def build_prompt(self, seed, nsfw, position, gesture, act_type, act):

        self.seed = seed
        prompt = ""

        if nsfw:
            prompt = self.build_nsfw_action(act_type, act)
        else:
            prompt = self.build_sfw_action(position, gesture)

        return (prompt,)

    def build_sfw_action(self, position, gesture):
        """Build a safe-for-work action prompt"""
        data = self.data["sfw"]

        position = self.select_tags(
            tags=data["positions"],
            selected=position
        )

        gesture = self.select_tags(
            tags=data["gestures"],
            selected=gesture
        )

        prompt = f"{position}, {gesture}"
        return prompt

    def build_nsfw_action(self, act_type, act):
        """Build a not-safe-for-work action prompt"""
        data = self.data["nsfw"]

        act_type = self.select_tags(
            tags=data["acts"],
            selected=act_type,
            recursive=False
        )

        act = self.select_tags(
            tags=data["acts"][act_type],
            selected=act
        )

        settings = self.apply_settings(data["settings"])
        prompt = self.enhance_prompt(data["acts"], act, settings)
        return prompt

    def apply_settings(self, data):
        """Apply NSFW settings"""
        settings = {}

        for key, value in data.items():
            settings[key] = self.select_tags(data[key])

        return settings

    def enhance_prompt(self, data, act_type, settings):
        """Enhance the NSFW action.
        Add or remove tags depending on the action type"""

        act = act_type
        if act_type in data:
            act = self.select_tags(data[act_type])

        penis, pussy = self.build_sex_parts(settings)
        sweat = "sweat"

        # Enhance act
        if act_type in data["intercourses"]:
            insertion = self.select_tags(settings["insertions"])
            act += f", {insertion}"

        # Enhance preliminary
        if act_type in data["preliminaries"]:
            if "fingering" in act_type:
                penis = ""
                if is_true(self.seed, 0.5):
                    act += ", fingering from behind"
            else:
                pussy = ""

        # Enhance teasing
        if "flashing" in act_type:
            # TODO: Add random body part flashing
            penis = ""
            pussy = ""
            act += ", nipples, clothes lift"

        components = [act, penis, pussy, sweat]
        act = self.stringify_tags(components)
        return act

    def build_sex_parts(self, settings):
        """Build sex parts, including penis, testicles, pussy, etc."""

        # Penis
        penis = f"{settings['penis_sizes']} penis"

        if settings["hide_male"]:
            penis += ", disembodied penis"

        # Testicles
        testicles = ""
        if is_true(self.seed, 0.3):
            testicles = f"{settings['testicles_sizes']} testicles"

        # Pussy
        pussy = "pussy"
        pussy_juice = "pussy juice"
        pussy_juice_weight = settings["pussy_juice"]

        if pussy_juice_weight >= 1:
            additional_tags = {
                "repeat": [1, 2],
                "tags": ["pussy juice trail", "pussy juice puddle"]
            }
            pussy_juice += ", " + self.select_tags(additional_tags)

        if pussy_juice_weight >= 1.1:
            pussy_juice = f"excessive {pussy_juice}"

        # Merge
        penis = self.stringify_tags([penis, testicles])
        pussy = self.stringify_tags([pussy, pussy_juice])
        return penis, pussy
