bl_info = {
    "name": "Blender Timelapse Tool",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
from . import timelapse_addon

def register():
    timelapse_addon.register()

def unregister():
    timelapse_addon.unregister()

if __name__ == "__main__":
    register()