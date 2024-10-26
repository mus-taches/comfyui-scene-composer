import argparse
import random
from src.scene import Scene


def main(seed, nsfw):

    if not seed:
        seed = random.randint(0, 0xffffffffffffffff)

    scene = Scene()
    scene.components["action"]["default"].INPUT_TYPES()
    output = scene.build_prompt(seed)

    print(f"SEED: {seed}")
    print(f"TAGS: {output}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Simulate a scene")

    parser.add_argument(
        "--seed", "-s",
        type=int,
        default=0,
        help="Seed for the node"
    )

    parser.add_argument(
        "--nsfw", "-n",
        type=bool,
        default=False,
        help="Whether the scene is NSFW"
    )

    args = parser.parse_args()
    main(args.seed, args.nsfw)
