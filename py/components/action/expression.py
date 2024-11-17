from ...node import Node


class Expression(Node):

    def __init__(self, seed, ident, rng):
        super().__init__(seed, data_file="actions.toml")
        self.rng = rng

    def build_prompt(self):
        data = self.data["expressions"]
        eyes = self.select_tags(data["eyes"])

        if eyes:
            eyes += " eyes"
            if "wink" in eyes:
                eyes = "one eye closed"

        looking = self.select_tags(data["looking"])
        if looking:
            looking = f"looking {looking}"

        mouth = self.select_tags(data["mouth"])

        if mouth:
            mouth += " mouth"
            if "half-closed" in mouth:
                mouth = "parted lips"

        tongue = self.select_tags(data["tongue"])

        self.components = {
            'eyes': eyes,
            'looking': looking,
            'mouth': mouth,
            'tongue': tongue
        }

        prompt = self.stringify_tags(self.components.values())
        return prompt
