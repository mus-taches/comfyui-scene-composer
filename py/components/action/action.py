from ...node import Node
from .expression import Expression
from .sfw import SFW
from .nsfw import NSFW


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
        acts = cls().build_acts(data["nsfw"]["acts"], act_types)
        acts = cls().build_inputs_list(acts)
        stages = ["imminent", "ongoing", "climax", "finish"]
        stages = cls().build_inputs_list(stages)

        # Update the required inputs
        inputs["required"] = {
            "nsfw": ("BOOLEAN", {"default": False}),
            # SFW inputs
            "position": (positions,),
            "gesture": (gestures,),
            # NSFW inputs
            "act_type": (act_types,),
            "act": (acts,),
            "stage": (stages,),
            "seed": seed
        }

        return inputs

    def build_prompt(self, seed, ident, nsfw, position, gesture,
                     act_type, act, stage):

        # Init RNG
        super().build_prompt(seed)

        # Client communication
        self.comfy_message("cozy-event-combo-update", ident, {
            "id": ident,
            "a": act_type,
            "b": act
        })

        # Build components
        expression = Expression(self.seed, ident, self.rng)
        sfw = SFW(self.seed, ident, self.rng)
        nsfw_class = NSFW(self.seed, ident, self.rng)

        action = ""
        if nsfw:
            action = nsfw_class.build_prompt(act_type, act, stage)
        else:
            action = sfw.build_prompt(position, gesture)

        self.components = {
            'expression': expression.build_prompt(),
            'action': action
        }

        prompt = self.stringify_tags(self.components.values())
        return (prompt,)

    def build_acts(cls, data, act_types):
        """Build a list of all acts from the data"""
        acts = []
        for act_type in act_types:
            if act_type == "random":
                continue
            if act_type not in data:
                act_type = cls().select_tags(
                    tags=data,
                    selected=act_type,
                    recursive=False
                )
            for act in data[act_type]:
                acts.extend([f"{act}"])
        return acts
