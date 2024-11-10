// https://github.com/cozy-comfyui/cozy_spoke

import { api } from "../../../scripts/api.js";
import { app } from "../../../scripts/app.js";

const _id = "Action"
const _root = "cozy_spoke"
const EVENT_COZY_UPDATE = "cozy-event-combo-update";

async function apiRoute(route, data = null, id = null) {
    const full_route = `/${_root}/${route}`;
    var blob = {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    }

    // if we are passing data, or need a specific node by ID, we must use a POST
    if (data != null || id != null) {
        blob['method'] = "POST",
            blob['body'] = JSON.stringify({
                id: id,
                data: data
            });
    }

    try {
        const response = await api.fetchApi(`${full_route}`, blob);
        if (!response.ok) {
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }
        return response;

    } catch (error) {
        console.error("API call to Jovimetrix failed:", error);
        throw error; // or return { success: false, message: error.message }
    }
}

app.registerExtension({
    name: 'cozy.spoke.' + _id,
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== _id) {
            return
        }

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = async function () {
            const me = onNodeCreated?.apply(this);
            const widget_dropdownA = this.widgets.find(w => w.name == 'act_type');
            const widget_dropdownB = this.widgets.find(w => w.name == 'act');

            widget_dropdownA.callback = async () => {
                try {
                    // Ask Python for the values we need to update widget_dropdownB
                    const response = await apiRoute("node", widget_dropdownA.value);
                    const responseData = await response.json();
                    widget_dropdownB.options.values = responseData.data;
                    widget_dropdownB.value = responseData.data[0];
                    this.setDirtyCanvas(true, true);
                } catch (error) {
                    console.error('Error in Dropdown A callback:', error);
                }
            }

            // process the message sent from python.
            // this could be during node execution or outside of it.
            async function python_update(data) {
                // Assuming you will do something with the data from Python here
                console.info('Received update from Python for Dropdown B:', data);
            }

            // catch the event(s) from python.
            api.addEventListener(EVENT_COZY_UPDATE, python_update);

            // clean up your mess when leaving.
            this.onDestroy = () => {
                api.removeEventListener(EVENT_COZY_UPDATE, python_update);
            };
            return me;
        }
    }
})