# renamer/operations/rename.py
import re
import maya.cmds as cmds
import uuid
from utils.undo import undo_chunk

from utils.maya_utils import (
    get_selected_uuids,
    get_hierarchy_uuids,
    get_selection,
    get_short_name
)

NUMBER_TOKEN_PATTERN = re.compile(
    r"_(\d+)_"
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


def build_renumber_plan(
    nodes,
    offset
):
    if not nodes:
        raise ValueError("No objects selected.")

    rename_data = []
    for node in nodes:
        short_name = node.split("|")[-1]
        match = NUMBER_TOKEN_PATTERN.search(short_name)

        if not match:
            raise ValueError(
                f"No '_##_'-style number found in: "
                f"{short_name}"
            )

        number_string = match.group(1)
        padding = len(number_string)
        old_number = int(number_string)

        new_number = (old_number + offset)

        if new_number < 0:
            raise ValueError(
                f"Resulting number would be negative for "
                f"{short_name}: "
                f"{old_number} + {offset}"
            )

        new_number_string = (str(new_number).zfill(padding))

        new_name = (
            short_name[:match.start(1)]
            + new_number_string
            + short_name[match.end(1):]
        )

        uuids = cmds.ls(
            node,
            uuid=True
        ) or []

        if not uuids:

            raise ValueError(
                f"Could not get UUID for: "
                f"{short_name}"
            )

        rename_data.append(
            {
                "uuid": uuids[0],
                "node": node,
                "short_name": short_name,
                "old_number": old_number,
                "new_name": new_name
            }
        )

    if offset > 0:
        rename_data.sort(
            key=lambda item:
            item["old_number"],
            reverse=True
        )

    elif offset < 0:
        rename_data.sort(
            key=lambda item:
            item["old_number"]
        )

    return rename_data


def _node_from_uuid(uuid_value):
    matches = cmds.ls(
        uuid_value,
        long=True
    ) or []

    if not matches:
        return None
    return matches[0]


@undo_chunk
def renumber_underscore_selection(offset):
    selection = cmds.ls(
        selection=True,
        long=True
    ) or []

    try:
        rename_data = build_renumber_plan(selection, offset)

    except ValueError as error:

        cmds.error(str(error))

        return []

    temp_token = uuid.uuid4().hex

    # --------------------------------------------------
    # First pass: rename everything to unique temp names.
    # This avoids collisions like:
    #
    # char_arm_01_jnt -> char_arm_02_jnt
    # char_arm_02_jnt -> char_arm_03_jnt
    # --------------------------------------------------

    for index, data in enumerate(rename_data):
        current_node = _node_from_uuid(data["uuid"])
        if not current_node:
            cmds.error(
                f"Could not find node: "
                f"{data['short_name']}"
            )

            return []

        temp_name = (
            f"tmpRenumber_"
            f"{temp_token}_"
            f"{index:04d}"
        )

        cmds.rename(current_node, temp_name)

    # --------------------------------------------------
    # Second pass: rename temp nodes to final names.
    # UUID lookup keeps this safe even if DAG paths changed.
    # --------------------------------------------------

    renamed_nodes = []

    for data in rename_data:
        current_node = _node_from_uuid(data["uuid"])
        if not current_node:
            cmds.error(
                f"Could not find temporary node for: "
                f"{data['short_name']}"
            )
            return []

        renamed_node = cmds.rename(current_node, data["new_name"])
        renamed_nodes.append(renamed_node)
    cmds.select(renamed_nodes, replace=True)

    return renamed_nodes