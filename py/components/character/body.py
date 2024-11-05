from ...node import Node


class Body(Node):

    def __init__(self, seed, rng):
        super().__init__(seed, data_file="character.toml")
        self.rng = rng

    def build_prompt(self):
        data = self.data["body"]
        type = self.select_tags(data["types"])
        colors = self.select_tags(data["colors"])
        color = f"{colors} skin" if colors else ""

        breasts_data = self.data["body"]["breasts"]
        breasts_size = self.select_tags(breasts_data["sizes"])
        breasts_prompt = f"{breasts_size}"

        extras = self.select_tags(data["extras"])
        extras = self.enhance_extras(extras)

        components = [type, color, breasts_prompt, extras]
        prompt = self.stringify_tags(components)
        return (prompt,)

    def enhance_extras(self, extras):
        prompt = ""
        match extras:
            case "tatoos":
                emplacement = ["arm", "leg", "back", "neck", "full-body"]
                emplacement = self.select_tags(emplacement)
                prompt = f"{emplacement} tatoo"
            case "piercings":
                emplacement = ["ear", "nose", "navel", "lip", "eyelid"]
                emplacement = self.select_tags(emplacement)
                prompt = f"{emplacement} piercing"
        return prompt
