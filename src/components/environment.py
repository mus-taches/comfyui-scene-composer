from ..node import Node


class Environment(Node):

    def __init__(self, seed=0):
        super().__init__(seed, data_file="environment.toml")

    def build_prompt(self, seed):
        self.seed = seed

        time = self.select_tags(self.data["time"])
        location_type = self.select_tags(self.data["locations"]["list"])
        location = self.select_tags(self.data["locations"][location_type])
        effects = self.select_tags(self.data["effects"])
        weather = self.build_weather(location)

        components = [time, effects, weather, location]

        if location_type == "indoors":
            components.remove(weather)

        prompt = ", ".join(components)
        return (prompt,)

    def build_weather(self, location):
        weather = self.data["weather"]

        if location == "beach":
            remove_from_list = ["snow", "rain"]
            weather = [w for w in weather if w not in remove_from_list]

        prompt = self.select_tags(weather)
        return prompt
