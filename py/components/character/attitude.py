from ...node import Node


class Attitude(Node):

    def __init__(self, seed, ident, rng):
        super().__init__(seed, data_file="character.toml")
        self.rng = rng

    def build_prompt(self):
        attitude = self.select_tags(self.data["attitudes"])
        prompt = attitude
        match attitude:
            case "happy":
                prompt += ", smile"
            case "smirk":
                prompt += ", smile, smug"
            case "bored":
                extra_tags = ["sleepy", "tired", "expressionless"]
                tags = self.select_tags(extra_tags, n=[1, 3])
                prompt += f", {tags}"
            case "upset":
                prompt += ", sad, angry, frown"
            case "crazy":
                prompt += ", crazy eyes, crazy smile, constricted pupils"
        return (prompt,)
