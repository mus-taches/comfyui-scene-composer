from ...node import Node


class Body(Node):

    def __init__(self, seed):
        super().__init__(seed, data_file="character.toml")

    def build_prompt(self):
        data = self.data["body"]
        type = self.select_tags(data["types"])
        colors = self.select_tags(data["colors"])
        color = f"{colors} skin" if colors else ""

        breasts_data = self.data["body"]["breasts"]
        breasts_size = self.select_tags(breasts_data["sizes"])
        breasts_prompt = f"{breasts_size}"

        extras = self.select_tags(data["extras"])

        components = [type, color, breasts_prompt, extras]
        prompt = self.stringify_tags(components)
        return (prompt,)
