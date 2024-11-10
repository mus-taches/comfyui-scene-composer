from ...node import Node

from .body import Body
from .hair import Hair
from .eyes import Eyes
from .attitude import Attitude


class Character(Node):

    def build_prompt(self, seed, ident):
        super().build_prompt(seed)

        components = {
            'body': Body(self.seed, ident, self.rng),
            'hair': Hair(self.seed, ident, self.rng),
            'eyes': Eyes(self.seed, ident, self.rng),
            'attitude': Attitude(self.seed, ident, self.rng)
        }

        prompt = ", ".join(str(component) for component in components.values())
        prompt = str(prompt)
        return (prompt,)
