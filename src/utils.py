from pathlib import Path
import numpy as np

ROOT_DIR = Path(__file__).parent.parent


def is_true(seed, p=0.5):
    """Return True with probability p"""
    rng = np.random.default_rng(seed)
    return rng.random() < p
