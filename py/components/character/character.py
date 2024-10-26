from ...node import Node

from .body import Body
from .hair import Hair
from .eyes import Eyes


class Character(Node):

    def build_prompt(self, seed):

        components = {
            'body': Body(seed),
            'hair': Hair(seed),
            'eyes': Eyes(seed)
        }

        prompt = ", ".join(str(component) for component in components.values())
        prompt = str(prompt)
        return (prompt,)
