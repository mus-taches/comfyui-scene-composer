from ...node import Node


class NSFW(Node):

    def __init__(self, seed, ident, rng):
        super().__init__(seed, data_file="actions.toml")
        self.rng = rng

    def build_prompt(self, act_type, act, stage):
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
        act = self.build_act_prompt(data["acts"], act, settings)

        self.components = {"act": act}

        prompt = self.stringify_tags(self.components.values())
        return prompt

    def apply_settings(self, data):
        """Apply NSFW settings"""
        settings = {}

        for key in data.keys():
            settings[key] = self.select_tags(data[key])

        return settings

    def build_act_prompt(self, data, act_type, settings):
        """Enhance the NSFW action.
        Add or remove tags depending on the action type"""

        act = act_type
        if act_type in data:
            act = self.select_tags(data[act_type])

        penis, pussy = self.build_sex_parts(settings)
        sweat = "sweat"

        # Enhance intercourses
        if act_type in data["intercourses"]:
            insertion = self.select_tags(settings["insertions"])
            act += f", {insertion}"

        # Enhance preliminary
        if act_type in data["preliminaries"]:
            if "fingering" in act_type:
                penis = ""
                if self.rng.random() < 0.5:
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
        if self.rng.random() < 0.3:
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
