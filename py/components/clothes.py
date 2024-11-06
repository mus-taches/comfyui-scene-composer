from ..node import Node


class Clothes(Node):

    def __init__(self, seed=0, state="clothed", type="random"):
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
                cloth = self.build_clothes(type)
            case "underwear":
                cloth = self.build_underwear()
            case "nude":
                cloth = "nude"

        accessories = self.build_accessory()
        prompt = f"{cloth}, {accessories}"

        return (prompt,)

    def build_clothes(self, type):
        prompt = ""
        match type:
            case "casual":
                colors = self.data["colors"]
                items = self.data["casual"]

                vest = self.build_piece(colors, items["vest"])
                top = self.build_piece(colors, items["top"])
                bottom = self.build_piece(colors, items["bottom"])

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

    def build_piece(self, colors, items):

        color = self.select_tags(colors)
        item = self.select_tags(items)
        piece = f"{color} {item}"

        if item == "":
            piece = ""

        return piece

    def build_accessory(self):

        accessories = self.select_tags(self.data["accessories"])
        colors = self.data["colors"]
        accessory = self.build_piece(colors, accessories.split(","))
        return accessory
