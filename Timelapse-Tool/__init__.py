bl_info = {
    "name": "Blender Timelapse Tool",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
from . import timelapse

def register():
    timelapse.register()

def unregister():
    timelapse.unregister()

if __name__ == "__main__":
    register()