from ...node import Node


class Body(Node):

    def __init__(self, seed, ident, rng):
        super().__init__(seed, data_file="character.toml")
        self.rng = rng

    def build_prompt(self):
        data = self.data["body"]
        type = self.select_tags(data["types"])
        colors = self.select_tags(data["colors"])
        color = f"{colors} skin" if colors else ""

        breasts_data = data["breasts"]
        breasts_size = self.select_tags(breasts_data["sizes"])
        breasts_prompt = f"{breasts_size}"

        lipstick = self.select_tags(self.data["mouth"]["lipstick"])
        if lipstick:
            lipstick_color = self.select_tags(
                self.data["mouth"]["lipstick"]["colors"])
            lipstick = f"{lipstick_color} lipstick"

        extras = self.select_tags(data["extras"])
        extras = self.enhance_extras(extras)

        components = [type, color, breasts_prompt, lipstick, extras]
        prompt = self.stringify_tags(components)
        return (prompt,)

    def enhance_extras(self, extras):
        prompt = ""
        match extras:
            case "mole":
                location = ["under eye", "under mouth", "on neck"]
                location = self.select_tags(location)
                prompt = f"mole {location}"
            case "tatoos":
                location = ["arm", "leg", "back", "neck", "full-body"]
                location = self.select_tags(location)
                prompt = f"{location} tatoo"
            case "piercings":
                location = ["ear", "nose", "navel", "lip", "eyelid"]
                location = self.select_tags(location)
                prompt = f"{location} piercing"
            case "scar":
                location = ["on neck", "on face", "on arm", "on forhead",
                            "on cheek", "accross eye", "on nose"]
                location = self.select_tags(location, n=[1, 2])
                prompt = f"scar {location}"
        return prompt
