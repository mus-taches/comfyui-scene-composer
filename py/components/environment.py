from ..node import Node


class Environment(Node):

    def __init__(self, seed=0):
        super().__init__(seed, data_file="environment.toml")

    def build_prompt(self, seed, ident):
        super().build_prompt(seed)

        time = self.select_tags(self.data["time"])
        location_type = self.select_tags(self.data["locations"]["list"])
        location = self.select_tags(self.data["locations"][location_type])
        effects = self.select_tags(self.data["effects"])
        weather = self.build_weather(time, location)

        self.components = {
            "time": time,
            "effects": effects,
            "weather": weather,
            "location_type": location_type,
            "location": location
        }

        if location_type == "indoors":
            self.components.pop("weather")

        prompt = self.stringify_tags(self.components.values())
        return (prompt,)

    def build_weather(self, time, location):
        weather = self.data["weather"]
        remove_from_list = []

        if time == "night":
            remove_from_list += ["sun"]

        if location == "beach":
            remove_from_list += ["snow", "rain"]

        weather = [w for w in weather if w not in remove_from_list]

        prompt = self.select_tags(weather)
        return prompt
