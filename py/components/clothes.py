from ..node import Node


class Clothes(Node):

    def __init__(self, seed=0, state="random", type="random"):
        super().__init__(seed, data_file="clothes.toml")
        self.state = state
        self.type = type

    def build_prompt(self, seed):
        super().build_prompt(seed)
        prompt = ""

        state = self.select_tags(self.data["states"], selected=self.state)
        type = self.select_tags(self.data["types"], selected=self.type)

        match state:
            case "clothed":
                prompt = self.build_clothes(type)
            case "underwear":
                prompt = self.build_underwear()
            case "nude":
                prompt = "nude"

        return (prompt,)

    def build_clothes(self, type):
        prompt = ""
        match type:
            case "casual":
                vest = Piece(self.data, "vest", self.rng)
                top = Piece(self.data, "top", self.rng)
                bottom = Piece(self.data, "bottom", self.rng)
                prompt = f"{vest}, {top}, {bottom}"

            case "dress":
                suffix = "dress"
                color = self.select_tags(self.data["colors"])
                length = self.select_tags(self.data["dress"]["length"])
                style = self.select_tags(self.data["dress"]["style"])
                prompt = (f"{color} {suffix}, "
                          f"{length} {suffix}, "
                          f"{style} {suffix}")

            case "swimsuit":
                color = self.select_tags(self.data["colors"])
                type = self.select_tags(self.data["swimsuit"])
                prompt = f"{color} swimsuit, {type}"

            case "uniform":
                color = self.select_tags(self.data["colors"])
                type = self.select_tags(self.data["uniform"])
                prompt = f"{color} uniform, {type} uniform"

            case _:
                color = self.select_tags(self.data["colors"])
                type = self.select_tags(self.data[self.type])
                prompt = f"{color} {type}"
        return prompt

    def build_underwear(self):
        color = self.select_tags(self.data["colors"])
        prompt = f"{color} bra, {color} panties"
        return prompt


class Piece(Node):
    """Return a colored piece of clothing"""

    def __init__(self, data, type, rng):
        self.rng = rng
        self.data = data
        self.type = type

    def build_prompt(self):
        color = self.select_tags(self.data["colors"])
        type = self.select_tags(self.data["casual"][self.type])
        piece = f"{color} {type}"

        if type == "":
            piece = ""

        prompt = f"{piece}"
        return prompt

    def __str__(self):
        return self.build_prompt()
