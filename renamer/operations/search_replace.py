# operations/search_replace.py

import maya.cmds as cmds

from utils.undo import undo_chunk
from operations.rename import (
    get_selection,
    get_hierarchy_selection,
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

    nodes = []

    if mode == "selected":

        nodes = get_selection()

    elif mode == "hierarchy":

        descendants, roots = (
            get_hierarchy_selection()
        )

        nodes = descendants + roots

    elif mode == "all":

        nodes = cmds.ls(
            long=True
        ) or []

    for node in nodes:

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