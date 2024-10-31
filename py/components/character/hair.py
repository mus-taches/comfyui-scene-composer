from ...node import Node


class Hair(Node):

    def __init__(self, seed, rng):
        super().__init__(seed, data_file="character.toml")
        self.rng = rng

    def build_prompt(self):
        data = self.data["hair"]
        suffix = "hair"

        color = self.select_tags(data["colors"])
        length = self.select_tags(data["lengths"])
        style = self.select_tags(data["styles"])

        prompt = f"{color} {suffix}, {length} {suffix}, {style}"
        return (prompt,)
