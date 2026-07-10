# operations/search_replace.py

import maya.cmds as cmds

from utils.undo import undo_chunk

from utils.maya_utils import (
    get_uuids_from_nodes,
    get_selected_uuids,
    get_hierarchy_uuids,
    get_short_name
)

@undo_chunk
def search_replace(
    search_text,
    replace_text,
    mode="selected"
):

    if not search_text:
        cmds.warning(
            "Search field is empty."
        )
        return

    uuids = []

    if mode == "selected":

        uuids = get_selected_uuids()

    elif mode == "hierarchy":

        uuids = get_hierarchy_uuids()

    elif mode == "all":

        uuids = get_uuids_from_nodes(
            cmds.ls(long=True) or []
        )

    for uuid in uuids:

        node = cmds.ls(
            uuid,
            long=True
        )

        if not node:
            continue

        node = node[0]

        short_name = get_short_name(node)

        if search_text not in short_name:
            continue

        new_name = short_name.replace(
            search_text,
            replace_text
        )

        cmds.rename(
            node,
            new_name
        )


def left_to_right(mode="selected"):

    search_replace(
        "l_",
        "r_",
        mode
    )


def right_to_left(mode="selected"):

    search_replace(
        "r_",
        "l_",
        mode
    )
def set_l_to_r_values(self):

    self.search_line.setText("l_")
    self.replace_line.setText("r_")


def set_r_to_l_values(self):

    self.search_line.setText("r_")
    self.replace_line.setText("l_")