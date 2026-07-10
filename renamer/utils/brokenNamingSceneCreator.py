import maya.cmds as cmds

cmds.file(new=True, force=True)

# -----------------------------
# GOOD JOINT CHAIN
# -----------------------------

root = cmds.joint(name="char_root_jnt")
cmds.joint(name="char_spine_01_jnt")
cmds.joint(name="char_spine_02_jnt")
cmds.joint(name="char_spine_03_jnt")

cmds.select(clear=True)

# -----------------------------
# PREFIX TYPO CHAIN
# -----------------------------

root = cmds.joint(name="char_arm_01_jnt")
cmds.joint(name="char_arm_02_jnt")
cmds.joint(name="chr_arm_03_jnt")      # typo
cmds.joint(name="char_arm_04_jnt")

cmds.select(clear=True)

# -----------------------------
# SUFFIX TYPO GROUP
# -----------------------------

cmds.group(empty=True, name="vehicle_body_geo")
cmds.group(empty=True, name="vehicle_wheel_FL_geo")
cmds.group(empty=True, name="vehicle_wheel_FR_geo")

cmds.group(
    empty=True,
    name="vehicle_wheel_RL_goe"   # typo
)

# -----------------------------
# NUMBERING ISSUES
# -----------------------------

cmds.group(empty=True, name="tentacle_01_ctrl")
cmds.group(empty=True, name="tentacle_02_ctrl")
cmds.group(empty=True, name="tentacle_03_ctrl")
cmds.group(empty=True, name="tentacle_17_ctrl")
cmds.group(empty=True, name="tentacle_05_ctrl")

# -----------------------------
# SIDE ISSUES
# -----------------------------

cmds.group(empty=True, name="L_arm_ctrl")
cmds.group(empty=True, name="L_hand_ctrl")
cmds.group(empty=True, name="Left_fingers_ctrl")  # inconsistent
cmds.group(empty=True, name="R_arm_ctrl")

# -----------------------------
# MISSING SUFFIXES
# -----------------------------

cmds.group(empty=True, name="char_helmet")
cmds.group(empty=True, name="char_sword")

# -----------------------------
# GEO OBJECTS
# -----------------------------

cube = cmds.polyCube(
    name="character_body_geo"
)[0]

sphere = cmds.polySphere(
    name="character_head_geo"
)[0]

cylinder = cmds.polyCylinder(
    name="character_arm_geoo"   # typo
)[0]

# -----------------------------
# MIXED FAMILY
# -----------------------------

cmds.group(empty=True, name="prop_chair_geo")
cmds.group(empty=True, name="prop_table_geo")

cmds.group(
    empty=True,
    name="props_lamp_geo"  # typo
)

# -----------------------------
# HUGE NUMBERING GAP
# -----------------------------

cmds.group(empty=True, name="rope_001_jnt")
cmds.group(empty=True, name="rope_002_jnt")
cmds.group(empty=True, name="rope_003_jnt")
cmds.group(empty=True, name="rope_015_jnt")

print("Validation test scene created.")