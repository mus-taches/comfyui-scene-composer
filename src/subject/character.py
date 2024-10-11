from ..node import Node

from ..subject.body import Body
from ..subject.hair import Hair
from ..subject.eyes import Eyes
from ..subject.clothes import Clothes


class Character(Node):

    def __init__(self, seed):
        super().__init__(seed)
        self.components = {
            'body': Body(self.seed),
            'hair': Hair(self.seed),
            'eyes': Eyes(self.seed),
            'clothes': Clothes(self.seed)
        }