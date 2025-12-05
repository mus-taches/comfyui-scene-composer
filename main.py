import argparse

from py.nodes.node_factory import NodeFactory
from py.utils.config import load_config

from py.nodes.apply_rules import ApplyRules

config = load_config()


def main(seed, verbose, with_inputs, with_rules, node_output):

    rules = ApplyRules()

    # Dislpay seed
    if 0 != seed:
        print(f"SEED: {seed}")
        print("---")

    # Create prompt for each node
    prompts = []
    nodes_variables = {}
    for key, value in config.items():
        ClassNode = NodeFactory.create_node(key)
        node = ClassNode()

        node_name = value.get("name", key)
        inputs = node.INPUT_TYPES()["required"]
        if "seed" in inputs:
            del inputs["seed"]
        prompt = node.build_prompt(seed=seed)

        if verbose:
            print(f"{node_name:<20} {prompt[0]}")

        # Optionally display inputs
        if with_inputs:
            for sub_key, sub_value in inputs.items():
                if isinstance(sub_value[0], list):
                    sub_value = sub_value[0]
                elif isinstance(sub_value[0], str):
                    sub_value = sub_value[1]["default"]
                    if sub_value is True:
                        sub_value = "Boolean"
                print(f"> {sub_key:<20} {sub_value}")
            print("---")
        nodes_variables.update(prompt[1])
        nodes_variables.update({node.__class__.__name__: prompt[0]})
        prompts.append(prompt[0])

    # Final prompt output
    if node_output is not False:
        OutputNode = NodeFactory.create_node(node_output)
        output_node = OutputNode()
        prompt = output_node.build_prompt(
            seed=seed, variables=nodes_variables)[0]
    else:
        prompt = ",".join(prompts)

    if with_rules:
        prompt = rules.apply_rules(prompt, "all", seed)

    print(prompt)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate a prompt from a node."
    )

    parser.add_argument(
        "-s", "--seed",
        type=int,
        default=0,
        help="Seed value for random number generator"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Split each node's prompt"
    )

    parser.add_argument(
        "-i", "--inputs",
        action="store_true",
        help="Display inputs for each node"
    )

    parser.add_argument(
        "-r", "--rules",
        action="store_true",
        help="Apply rules"
    )

    parser.add_argument(
        "-n", "--node",
        type=str,
        default=False,
        help="Name of the node to output"
    )

    args = parser.parse_args()

    main(
        seed=args.seed,
        verbose=args.verbose,
        with_inputs=args.inputs,
        with_rules=args.rules,
        node_output=args.node
    )
