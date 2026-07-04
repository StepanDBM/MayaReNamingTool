import maya.cmds as cmds

from utils.undo import undo_chunk

@undo_chunk
def apply_viewport_color(r, g, b):

    selection = cmds.ls(selection=True, long=True) or []
    print(f"r: {r}, g: {g}, b: {b}")

    for obj in selection:
        node_type = cmds.nodeType(obj)

        # Joints
        if node_type == "joint":

            cmds.setAttr(f"{obj}.overrideEnabled", True)

            cmds.setAttr(f"{obj}.overrideRGBColors", True)

            cmds.setAttr(f"{obj}.overrideColorRGB", r, g, b)
        

        # Shapes
        shapes = cmds.listRelatives(
            obj,
            shapes=True,
            fullPath=True
        ) or []

        for shape in shapes:

            cmds.setAttr(f"{shape}.overrideEnabled", True)

            cmds.setAttr(f"{shape}.overrideRGBColors", True)

            cmds.setAttr(f"{shape}.overrideColorRGB", r, g, b)

@undo_chunk
def apply_outliner_color(r, g, b):

    selection = cmds.ls(selection=True, long=True) or []

    for obj in selection:

        cmds.setAttr(f"{obj}.useOutlinerColor", True)

        cmds.setAttr(f"{obj}.outlinerColor", r, g, b)

@undo_chunk
def reset_colors():

    selection = cmds.ls(selection=True, long=True) or []

    for obj in selection:

        try:
            cmds.setAttr(f"{obj}.useOutlinerColor", False)
        except:
            pass

        shapes = cmds.listRelatives(
            obj,
            shapes=True,
            fullPath=True
        ) or []

        for shape in shapes:

            try:
                cmds.setAttr(f"{shape}.overrideEnabled", False)
            except:
                pass