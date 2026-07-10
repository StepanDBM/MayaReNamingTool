# renamer/operations/rename.py
import re
import maya.cmds as cmds
from utils.undo import undo_chunk

from utils.maya_utils import (
    get_selected_uuids,
    get_hierarchy_uuids,
    get_selection,
    get_short_name
)



# Character Removal
@undo_chunk
def remove_character(position):

    selection = get_selection()

    for obj in reversed(selection):

        short_name = get_short_name(obj)

        if len(short_name) <= 1:
            continue

        if position == "first":
            new_name = short_name[1:]

        elif position == "last":
            new_name = short_name[:-1]

        else:
            raise ValueError(f"Invalid position: {position}")

        cmds.rename(obj, new_name)
        rename_shapes_for_nodes(get_selection())


# Quick Suffix
@undo_chunk
def quick_suffix(suffix):
    
    selection = get_selection()

    for obj in reversed(selection):

        short_name = get_short_name(obj)

        cmds.rename(obj, f"{short_name}{suffix}")
        rename_shapes_for_nodes(get_selection())

# Prefix
@undo_chunk
def add_prefix(prefix):
    
    if not prefix:
        cmds.warning("Prefix field is empty.")
        return

    selection = get_selection()

    for obj in reversed(selection):

        short_name = get_short_name(obj)

        cmds.rename(obj, f"{prefix}{short_name}")
        rename_shapes_for_nodes(get_selection())

@undo_chunk
def add_prefix_hierarchy(prefix):

    if not prefix:
        cmds.warning("Prefix field is empty.")
        return

    uuids = get_hierarchy_uuids()

    for uuid in uuids:

        obj = cmds.ls(uuid, long=True)

        if not obj:
            continue

        obj = obj[0]

        short_name = get_short_name(obj)

        cmds.rename(
            obj,
            f"{prefix}{short_name}"
        )

    rename_shapes_for_nodes(get_selection())

# Suffix
@undo_chunk
def add_suffix(suffix):
    """
    Adds suffix to selected nodes.
    """

    if not suffix:
        cmds.warning("Suffix field is empty.")
        return

    selection = get_selection()

    for obj in reversed(selection):

        short_name = get_short_name(obj)

        cmds.rename(obj, f"{short_name}{suffix}")
        rename_shapes_for_nodes(get_selection())

@undo_chunk
def add_suffix_hierarchy(suffix):

    if not suffix:
        cmds.warning("Suffix field is empty.")
        return

    uuids = get_hierarchy_uuids()

    for uuid in uuids:

        obj = cmds.ls(uuid, long=True)

        if not obj:
            continue

        obj = obj[0]

        short_name = get_short_name(obj)

        cmds.rename(
            obj,
            f"{short_name}{suffix}"
        )

    rename_shapes_for_nodes(get_selection())

@undo_chunk
def rename_and_number(
    base_name,
    start=1,
    padding=2
):

    if not base_name:
        cmds.warning("Rename field is empty.")
        return

    uuids = get_selected_uuids()

    for index, uuid in enumerate(uuids):

        obj = cmds.ls(uuid,long=True)

        if not obj:
            continue

        obj = obj[0]

        number = start + index

        padded = str(number).zfill(padding)

        new_name = (f"{base_name}{padded}")

        cmds.rename(obj, new_name)
        rename_shapes_for_nodes(get_selection())


@undo_chunk
def hash_rename(pattern):

    if not pattern:
        cmds.warning("Hash rename field is empty.")
        return

    match = re.search(r"#+", pattern)

    if not match:
        cmds.warning("Pattern contains no # characters.")
        return

    hashes = match.group()
    padding = len(hashes)

    # Store stable references
    uuids = get_selected_uuids()

    for index, uuid in enumerate(uuids, start=1):

        # Get current DAG path every iteration
        obj = cmds.ls(uuid, long=True)

        if not obj:
            continue

        obj = obj[0]

        number = str(index).zfill(padding)

        new_name = pattern.replace(
            hashes,
            number,
            1
        )

        cmds.rename(obj, new_name)
@undo_chunk
def rename_shapes_for_nodes(nodes):

    for transform in nodes:

        shapes = cmds.listRelatives(
            transform,
            shapes=True,
            fullPath=True
        ) or []

        transform_name = get_short_name(transform)

        for index, shape in enumerate(shapes, start=1):

            if len(shapes) == 1:

                new_shape_name = (f"{transform_name}Shape")

            else:

                new_shape_name = (f"{transform_name}Shape{index}")

            cmds.rename(shape, new_shape_name)


@undo_chunk
def strip_namespace():

    uuids = get_selected_uuids()

    for uuid in uuids:

        obj = cmds.ls(uuid, long=True)

        if not obj:
            continue

        obj = obj[0]

        short_name = get_short_name(obj)

        if ":" not in short_name:
            continue

        new_name = short_name.split(":")[-1]

        cmds.rename(obj, new_name)

    rename_shapes_for_nodes(get_selection())

@undo_chunk
def strip_namespace_hierarchy():

    uuids = get_hierarchy_uuids()

    for uuid in uuids:

        obj = cmds.ls(uuid, long=True)

        if not obj:
            continue

        obj = obj[0]

        short_name = get_short_name(obj)

        if ":" not in short_name:
            continue

        new_name = short_name.split(":")[-1]

        cmds.rename(
            obj,
            new_name
        )

    rename_shapes_for_nodes(get_selection())