from ...node import Node


class Hair(Node):

    def __init__(self, seed, rng):
        super().__init__(seed, data_file="character.toml")
        self.rng = rng

    def build_prompt(self):
        data = self.data["hair"]
        suffix = "hair"
        color = self.select_tags(data["colors"])
        if color == "gradient":
            color = self.enhance_gradient()

        length = self.select_tags(data["lengths"])
        style = self.select_tags(data["styles"])

        prompt = f"{color} {suffix}, {length} {suffix}, {style}"
        return (prompt,)

    def enhance_gradient(self):
        color_1 = self.select_tags(
            self.data["hair"]["colors"]["standard_colors"])
        color_2 = self.select_tags(
            self.data["hair"]["colors"]["special_colors"])

        return f"gradient hair, {color_1} hair, {color_2}"
