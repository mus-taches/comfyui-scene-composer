from ...node import Node


class Attitude(Node):

    def __init__(self, seed, ident, rng):
        super().__init__(seed, data_file="character.toml")
        self.rng = rng

    def build_prompt(self):
        attitude = self.select_tags(self.data["attitudes"])
        match attitude:
            case "happy":
                attitude += ", smile"
            case "smirk":
                attitude += ", smile, smug"
            case "bored":
                extra_tags = ["sleepy", "tired", "expressionless"]
                tags = self.select_tags(extra_tags, n=[1, 3])
                attitude += f", {tags}"
            case "upset":
                attitude += ", sad, angry, frown"
            case "crazy":
                attitude += ", crazy eyes, crazy smile, constricted pupils"

        self.components = {
            "attitude": attitude
        }
        prompt = self.stringify_tags(self.components.values())
        return (prompt,)
