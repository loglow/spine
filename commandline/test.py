import bpy
import sys

bpy.ops.wm.open_mainfile(filepath=sys.argv[-1])
bpy.ops.wm.read_homefile()
print("GOOD")
