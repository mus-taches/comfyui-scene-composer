import { app } from "../../scripts/app.js";

let origProps = {};

const findWidgetByName = (node, name) => {
    return node.widgets ? node.widgets.find(w => w.name === name) : null;
};

const doesInputWithNameExist = (node, name) => {
    return false;
};

const HIDDEN_TAG = "tschide";

// Toggle Widget + change size
function toggleWidget(node, widget, show = false, suffix = "") {
    if (!widget || doesInputWithNameExist(node, widget.name)) return;

    // Store the original properties of the widget if not already stored
    if (!origProps[widget.name]) {
        origProps[widget.name] = {
            origType: widget.type,
            origComputeSize: widget.computeSize,
        };
    }

    const origSize = node.size;

    // Set the widget type and computeSize based on the show flag
    widget.type = show ? origProps[widget.name].origType : HIDDEN_TAG + suffix;

    widget.computeSize = show ? origProps[widget.name].origComputeSize : () => [0, -4];

    // A stupid fix to force textarea to hide
    widget.element.style.display = show ? "block" : "none";

    // Calculate the new height for the node based on its computeSize method
    const newHeight = node.computeSize()[1];
    node.setSize([node.size[0], newHeight]);
}

// Create a map of node titles to their respective widget handlers
const nodeWidgetHandlers = {
    "output": {
        output: toggleCustomOutput,
    },
};

// In the main function where widgetLogic is called
function widgetLogic(node, widget) {
    // Retrieve the handler function for the current node title and widget name
    // const handler = nodeWidgetHandlers[node.title]?.[widget.name];

    // Trigger toggleCustomOutput for each "output" widget
    if (widget.name === "output") {
        toggleCustomOutput(node, widget);
    }
}

function toggleCustomOutput(node, widget) {

    const custom_output = findWidgetByName(node, "custom_output");
    const output_value = widget.value;

    // Hide custom_output if the output is not "custom"
    toggleWidget(node, custom_output, output_value == "custom");
}

app.registerExtension({
    name: "scenecomposer.widgethider",
    nodeCreated(node) {
        for (const widget of node.widgets || []) {
            widget.callback = function () { widgetLogic(node, widget) }
        }
    },
});
