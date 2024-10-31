from ...node import Node


class Attitude(Node):

    def __init__(self, seed, rng):
        super().__init__(seed, data_file="character.toml")
        self.rng = rng

    def build_prompt(self):
        prompt = ""

        eyes = self.select_tags(self.data["expressions"]["eyes"])
        mouth = self.select_tags(self.data["expressions"]["mouth"])

        attitude = self.enhance_attitude(
            self.select_tags(self.data["attitudes"]))

        prompt += f"{eyes} eyes, {mouth} mouth, {attitude}"

        return (prompt,)

    def enhance_attitude(self, attitude):

        prompt = attitude
        match attitude:

            case "happy":
                prompt += ", smile"

            case "smirk":
                prompt += ", smile, smirk, smug"

            case "bored":
                prompt += ", sleepy, tired, expressionless"

            case "upset":
                prompt += ", upset, sad, angry, frown"

            case "crazy":
                prompt += ", crazy eyes, crazy smile, constricted pupils"

        return prompt
