from ...node import Node


class Attitude(Node):

    def __init__(self, seed, rng):
        super().__init__(seed, data_file="character.toml")
        self.rng = rng

    def build_prompt(self):
        attitude = self.select_tags(self.data["attitudes"])
        prompt = attitude
        match attitude:
            case "happy":
                prompt += ", smile"
            case "smirk":
                prompt += ", smile, smirk, smug"
            case "bored":
                prompt += ", sleepy, tired, expressionless"
            case "upset":
                prompt += ", sad, angry, frown"
            case "crazy":
                prompt += ", crazy eyes, crazy smile, constricted pupils"
        return (prompt,)
