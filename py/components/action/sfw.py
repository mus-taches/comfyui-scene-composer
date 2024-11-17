from ...node import Node


class SFW(Node):

    def __init__(self, seed, ident, rng):
        super().__init__(seed, data_file="actions.toml")
        self.rng = rng

    def build_prompt(self, position, gesture):
        data = self.data["sfw"]

        position = self.select_tags(
            tags=data["positions"],
            selected=position
        )

        gesture = self.select_tags(
            tags=data["gestures"],
            selected=gesture,
        )

        self.components = {
            'position': position,
            'gesture': gesture
        }

        prompt = self.stringify_tags(self.components.values())
        return prompt
