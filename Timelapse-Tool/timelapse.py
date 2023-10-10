import bpy
import os
from bpy_extras.io_utils import ExportHelper

bpy.types.Scene.timelapse_speed = bpy.props.FloatProperty(
    name="Timelapse Speed",
    description="Speed factor for the timelapse",
    default=2.0,
    min=1.0,
    max=10.0,
    soft_min=1.0,
    soft_max=10.0
)

bpy.types.Scene.timelapse_output_folder = bpy.props.StringProperty(
    name="Output Folder",
    description="Folder to save the timelapse",
    default="",
    subtype='DIR_PATH'
)

def start_timelapse(output_folder, frame_rate=24):
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.compression = 0
    bpy.context.scene.render.fps = frame_rate
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = bpy.context.scene.frame_end
    bpy.ops.screen.animation_play()
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.ffmpeg.codec = 'H264'
    bpy.context.scene.render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'
    bpy.context.scene.render.filepath = os.path.join(output_folder, 'timelapse.mp4')
    bpy.ops.render.render(animation=True)
    bpy.ops.screen.animation_cancel(restore_frame=False)
    bpy.context.scene.render.filepath = ''

def change_speed(speed):
    original_frame_end = bpy.context.scene.frame_end
    bpy.context.scene.frame_end = int(original_frame_end / speed)

class TimelapseOutputFolderOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "timelapse.output_folder"
    bl_label = "Select Output Folder"
    bl_options = {'REGISTER', 'PRESET'}

    filename_ext = ""

    def execute(self, context):
        output_folder = self.filepath
        bpy.context.scene.timelapse_output_folder = output_folder
        self.report({'INFO'}, f"Output folder selected: {output_folder}")
        return {'FINISHED'}

class TimelapseStartOperator(bpy.types.Operator):
    bl_idname = "timelapse.start"
    bl_label = "Start Timelapse"

    def execute(self, context):
        output_folder = context.scene.timelapse_output_folder
        timelapse_speed = context.scene.timelapse_speed

        if not output_folder:
            self.report({'ERROR'}, "Please select an output folder.")
            return {'CANCELLED'}

        try:
            start_timelapse(output_folder, frame_rate=24)
            change_speed(timelapse_speed)
            self.report({'INFO'}, "Timelapse completed successfully.")
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")

        return {'FINISHED'}

class TIMELAPSE_PT_panel(bpy.types.Panel):
    bl_label = "Timelapse Settings"
    bl_idname = "TIMELAPSE_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if scene.timelapse_output_folder:
            layout.operator("timelapse.output_folder", text=f"Output Folder: {scene.timelapse_output_folder}")
        else:
            layout.operator("timelapse.output_folder", text="Select Output Folder")

        layout.prop(scene, "timelapse_speed", text="Timelapse Speed")

        if not scene.timelapse_output_folder:
            layout.label(text="Select an output folder to enable Start Timelapse.")
        else:
            layout.operator("timelapse.start", text="Start Timelapse")

def register():
    bpy.utils.register_class(TimelapseOutputFolderOperator)
    bpy.utils.register_class(TIMELAPSE_PT_panel)
    bpy.utils.register_class(TimelapseStartOperator)

def unregister():
    bpy.utils.unregister_class(TimelapseOutputFolderOperator)
    bpy.utils.unregister_class(TIMELAPSE_PT_panel)
    bpy.utils.unregister_class(TimelapseStartOperator)

if __name__ == "__main__":
    register()
