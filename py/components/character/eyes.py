from ...node import Node


class Eyes(Node):

    def __init__(self, seed, rng):
        super().__init__(seed, data_file="character.toml")
        self.rng = rng

    def build_prompt(self):
        data = self.data["eyes"]
        suffix = "eyes"
        color = self.select_tags(data["colors"])
        eyewear = self.build_eyewear_prompt(data["eyewears"])

        prompt = f"{color} {suffix}, {eyewear}"
        return (prompt,)

    def build_eyewear_prompt(self, eyewear):
        p = eyewear["probability"]

        suffix = "eyewear"
        type = self.select_tags(eyewear["types"], p)
        color = self.select_tags(eyewear["colors"], p)
        colored_element = self.select_tags(["framed", "tinted"])

        tags = [
            f"{type}",
            f"{color}-{colored_element} {suffix}",
        ]

        eyewear_prompt = self.stringify_tags(
            tags) if self.rng.random() < p else ""
        return eyewear_prompt
