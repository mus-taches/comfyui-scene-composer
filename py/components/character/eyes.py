from ...node import Node


class Eyes(Node):

    def __init__(self, seed, ident, rng):
        super().__init__(seed, data_file="character.toml")
        self.rng = rng

    def build_prompt(self):
        data = self.data["eyes"]
        suffix = "eyes"
        color = self.select_tags(data["colors"])

        makeup = self.build_makeup_prompt(data["makeup"])
        eyewear = self.build_eyewear_prompt(data["eyewears"])

        prompt = f"{color} {suffix}, {makeup}, {eyewear}"
        return (prompt,)

    def build_makeup_prompt(self, data):
        makeup = ""
        makeup_type = self.select_tags(data)
        if makeup_type:
            makeup_color = self.select_tags(data["colors"])
            makeup = f"{makeup_color} {makeup_type}"
        return makeup

    def build_eyewear_prompt(self, eyewear):
        p = eyewear["probability"]

        suffix = "eyewear"
        type = self.select_tags(eyewear["types"], p)
        color = self.select_tags(eyewear["colors"], p)
        colored_element = "framed"

        if "goggles" in type:
            colored_element = "tinted"
            position = self.select_tags(["on head", "around neck"])
            type = f"{type}, {type} {position}"

        if "sunglasses" in type:
            colored_element = "tinted"

        tags = [
            f"{type}",
            f"{color}-{colored_element} {suffix}",
        ]

        eyewear_prompt = self.stringify_tags(
            tags) if self.rng.random() < p else ""
        return eyewear_prompt
