from ...node import Node


class Hair(Node):

    def __init__(self, seed, ident, rng):
        super().__init__(seed, data_file="character.toml")
        self.rng = rng

    def build_prompt(self):
        data = self.data["hair"]
        suffix = "hair"

        # Hair color
        color = self.select_tags(data["colors"])
        if color == "gradient":
            color = self.enhance_gradient()
        color = f"{color} {suffix}"

        # Hair length
        length = self.select_tags(data["lengths"])
        length = f"{length} {suffix}"

        # Hair style
        style = self.select_tags(data["styles"])
        style = f"{style} {suffix}"

        # Components
        self.components = {
            "color": color,
            "length": length,
            "style": style
        }
        prompt = self.stringify_tags(self.components.values())
        return (prompt,)

    def enhance_gradient(self):
        color_1 = self.select_tags(
            self.data["hair"]["colors"]["standard_colors"])
        color_2 = self.select_tags(
            self.data["hair"]["colors"]["special_colors"])

        return f"gradient hair, {color_1} hair, {color_2}"
