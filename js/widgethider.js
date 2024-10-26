import { app } from "../../scripts/app.js";

let origProps = {};

const findWidgetByName = (node, name) => {
  return node.widgets ? node.widgets.find(w => w.name === name) : null;
};

const doesInputWithNameExist = (node, name) => {
  return node.inputs ? node.inputs.some(input => input.name === name) : false;
};

const HIDDEN_TAG = "cschide";

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
  widget.computeSize = show
    ? origProps[widget.name].origComputeSize
    : () => [0, -4];

  // Calculate the new height for the node based on its computeSize method
  const newHeight = node.computeSize()[1];
  node.setSize([node.size[0], newHeight]);
}

// Create a map of node titles to their respective widget handlers
const nodeWidgetHandlers = {
  "🎬 Action": {
    nsfw: handleSceneNsfw,
  },
};

// In the main function where widgetLogic is called
function widgetLogic(node, widget) {
  // Retrieve the handler for the current node title and widget name
  const handler = nodeWidgetHandlers[node.comfyClass]?.[widget.name];
  if (handler) {
    handler(node, widget);
  }
}

// Show SFW/NSFW widgets according to the value of the "nsfw" widget
function handleSceneNsfw(node, widget) {
  const isNsfw = widget.value;
  const sfwWidgets = [
    findWidgetByName(node, `position`),
    findWidgetByName(node, `gesture`),
  ];
  const nsfwWidgets = [
    findWidgetByName(node, `act_type`),
    findWidgetByName(node, `act`),
  ];
  const allWidgets = [...sfwWidgets, ...nsfwWidgets];

  // Hide all widgets
  for (const w of allWidgets) {
    toggleWidget(node, w, false);
  }

  // Show the appropriate SFW/NSFW widgets
  const widgetsToToggle = isNsfw ? nsfwWidgets : sfwWidgets;
  for (const w of widgetsToToggle) {
    toggleWidget(node, w, true);
  }

  if (isNsfw) {
    // Dynamic act list based on the selected act_type
    const actWidget = findWidgetByName(node, `act`);
    const actTypeWidget = findWidgetByName(node, `act_type`);
    filterInputList(node, actWidget, actTypeWidget);
    actTypeWidget.callback = () =>
      filterInputList(node, actWidget, actTypeWidget);
  }
}

function filterInputList(node, actWidget, actTypeWidget) {
  // Restore original value
  if (origProps[actWidget.name].originalValues) {
    actWidget.options.values = origProps[actWidget.name].originalValues;
  }

  // Store original values before filtering
  if (origProps[actWidget.name]) {
    origProps[actWidget.name].originalValues = [...actWidget.options.values];
  }

  // Hide act widget if act_type is random
  toggleWidget(node, actWidget, actTypeWidget.value !== "random");

  // Filter the act list based on the selected act_type
  actWidget.options.values = actWidget.options.values
    .filter(act => act.startsWith(`${actTypeWidget.value}_`) || act == "random")
    .map(act => act.replace(`${actTypeWidget.value}_`, ""));

  // Set the value to the first act in the list
  actWidget.value = actWidget.options.values[0];
}

app.registerExtension({
  name: "scenecomposer.widgethider",
  nodeCreated(node) {
    for (const w of node.widgets || []) {
      let widgetValue = w.value;

      // Store the original descriptor if it exists
      let originalDescriptor = Object.getOwnPropertyDescriptor(w, "value");
      if (!originalDescriptor) {
        originalDescriptor = Object.getOwnPropertyDescriptor(
          w.constructor.prototype,
          "value"
        );
      }

      widgetLogic(node, w);

      Object.defineProperty(w, "value", {
        get() {
          // If there's an original getter, use it. Otherwise, return widgetValue.
          let valueToReturn =
            originalDescriptor && originalDescriptor.get
              ? originalDescriptor.get.call(w)
              : widgetValue;

          return valueToReturn;
        },
        set(newVal) {
          // If there's an original setter, use it. Otherwise, set widgetValue.
          if (originalDescriptor && originalDescriptor.set) {
            originalDescriptor.set.call(w, newVal);
          } else {
            widgetValue = newVal;
          }

          widgetLogic(node, w);
        },
      });
    }
  },
});
