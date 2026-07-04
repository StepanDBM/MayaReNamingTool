# renamer/operations/rename.py
import re
import maya.cmds as cmds
from utils.undo import undo_chunk

# Helpers

def get_selected_uuids():
    return cmds.ls(
        selection=True,
        uuid=True
    ) or []

def get_selection():
    """
    Return current selection as long names.

    Long names help prevent hierarchy renaming issues.
    """
    return cmds.ls(
        selection=True,
        long=True
    ) or []

def get_hierarchy_selection():
    """
    Returns:
        descendants (leaf -> root)
        selected roots
    """

    descendants = []

    selection = cmds.ls(
        selection=True,
        long=True
    ) or []

    for node in selection:

        children = cmds.listRelatives(
            node,
            allDescendents=True,
            fullPath=True
        ) or []

        descendants.extend(children)

    return descendants, selection

def get_short_name(node):
    """ ditch DAG path :: |...|group|cube_geo -> cube_geo
    """
    return node.split("|")[-1]


# Character Removal
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


# Quick Suffix
def quick_suffix(suffix):
    
    selection = get_selection()

    for obj in reversed(selection):

        short_name = get_short_name(obj)

        cmds.rename(obj, f"{short_name}{suffix}")


# Prefix
def add_prefix(prefix):
    
    if not prefix:
        cmds.warning("Prefix field is empty.")
        return

    selection = get_selection()

    for obj in reversed(selection):

        short_name = get_short_name(obj)

        cmds.rename(obj, f"{prefix}{short_name}")

@undo_chunk
def add_prefix_hierarchy(prefix):

    if not prefix:
        cmds.warning("Prefix field is empty.")
        return

    descendants, selection = get_hierarchy_selection()

    # Children first
    for node in descendants:

        short_name = get_short_name(node)

        cmds.rename(node, f"{prefix}{short_name}")

    # Then roots
    for node in selection:

        short_name = get_short_name(node)

        cmds.rename(node, f"{prefix}{short_name}")

# Suffix
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

@undo_chunk
def add_suffix_hierarchy(suffix):

    if not suffix:
        cmds.warning("Suffix field is empty.")
        return

    descendants, selection = get_hierarchy_selection()
    
    # Children first
    for node in descendants:

        short_name = get_short_name(node)

        cmds.rename(node, f"{short_name}{suffix}")

    # Then roots
    for node in selection:

        short_name = get_short_name(node)

        cmds.rename(node, f"{short_name}{suffix}")

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