# CozySpoke – Widget manipulation with API
# https://github.com/cozy-comfyui/cozy_spoke

import time
# import toml
# from pathlib import Path
from typing import Any
from aiohttp import web  # , ClientSession
from server import PromptServer

from ..node import Node

EVENT_COZY_UPDATE = "cozy-event-combo-update"


class TimedOutException(Exception):
    pass


class ComfyAPIMessage:
    """
    This is to collect messages from JS for nodes that are parsing/looking
    for messages.
    """
    MESSAGE = {}

    @classmethod
    def poll(cls, ident, period=0.01, timeout=3) -> Any:
        _t = time.monotonic()
        if isinstance(ident, (set, list, tuple, )):
            ident = ident[0]

        sid = str(ident)
        while not (sid in cls.MESSAGE) and time.monotonic() - _t < timeout:
            time.sleep(period)

        if not (sid in cls.MESSAGE):
            raise TimedOutException
        dat = cls.MESSAGE.pop(sid)
        return dat


def initialize_cozy_spoke():

    data = Node.load_data("actions.toml")

    @PromptServer.instance.routes.get("/cozy_spoke")
    async def route_cozy_spoke(request) -> Any:
        """A simple lookup for the data provided.
        The function names need to be unique for each 'route'.
        Returns all messages stored in the Message Bus.
        """
        return web.json_response(ComfyAPIMessage.MESSAGE)

    @PromptServer.instance.routes.post("/cozy_spoke")
    async def route_cozy_spoke_combo(request) -> Any:
        """A catch all route to pass messages for specific node messages needed
        during node execution. The node itself will search the message bucket
        and can process during its run function call."""
        json_data = await request.json()
        if (did := json_data.get("id")) is not None:
            # stores the data-call for the instanced node (by id)
            # to check on execute
            ComfyAPIMessage.MESSAGE[str(did)] = json_data
            return web.json_response(json_data)
        return web.json_response({})

    @PromptServer.instance.routes.post("/cozy_spoke/node")
    async def route_cozy_spoke_update(request) -> Any:
        """A specific route for a specific node
        to process outside of an execution run.
        Here we manipulate the values output based on the selection in ComboA
        """

        # Show/Hide widgets according to data dict
        json_data = await request.json()
        result = {}
        if (response := json_data.get("data")) is not None:
            acts = data["nsfw"]["acts"]
            selected_acts = acts.get(response.lower(), [])
            inputs = Node.build_inputs_list(selected_acts)
            result = {'data': inputs}

        return web.json_response(result)
