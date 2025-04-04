from .py.utils.config import load_config
from .py.nodes.node_factory import NodeFactory
from .py.nodes.merge_strings import MergeStrings
from .py.nodes.composer import Composer
from .py.nodes.cleanup_prompt import CleanupPrompt
from .py.nodes.apply_rules import ApplyRules

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "./web"


def register_node(node_id, node_name, node_class):
    NODE_CLASS_MAPPINGS[node_id] = node_class
    NODE_DISPLAY_NAME_MAPPINGS[node_id] = node_name


# Create each node according to the config folder
config = load_config()

for key, value in config.items():
    node_id = key
    node_name = value.get("name", key)
    ClassNode = NodeFactory.create_node(node_id, node_name)
    register_node(node_id, node_name, ClassNode)

# Add additional nodes
register_node("MergeStrings", "🪡 Merge Strings", MergeStrings)
register_node("Composer", "🖋️ Composer", Composer)
register_node("CleanupPrompt", "🧹 CleanUp Prompt", CleanupPrompt)
register_node("ApplyRules", "📋 Apply Rules", ApplyRules)

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY"
]
