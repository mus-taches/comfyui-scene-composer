from ...node import Node

from .body import Body
from .hair import Hair
from .eyes import Eyes


class Character(Node):

    def build_prompt(self, seed):
        super().build_prompt(seed)

        components = {
            'body': Body(self.seed),
            'hair': Hair(self.seed),
            'eyes': Eyes(self.seed)
        }

        prompt = ", ".join(str(component) for component in components.values())
        prompt = str(prompt)
        return (prompt,)
