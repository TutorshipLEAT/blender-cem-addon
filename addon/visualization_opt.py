import bpy
import os

from bpy.types import Context, Event
from bpy_extras.io_utils import ImportHelper


class OBJECT_PT_visualization_section(bpy.types.Panel):
    bl_label = 'Visualization'
    bl_idname = 'OBJECT_PT_visualization_section'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CEM'

    def draw(self, context):
        layout = self.layout
        self.draw_visualization_section(context, layout)

    def draw_visualization_section(self, context, layout):
        row = layout.row()
        row.label(text='Visualization', icon='MOD_WAVE')

        col = layout.column()
        col.prop(context.scene, 'visualization_types', text="")

        row = layout.column()
        row.operator('visualization.open_filebrowser',
                     text="Select .txt File", icon="FILEBROWSER")

        if (context.scene.data_file_path):
            row = layout.row()
            row.label(text=f'Selected file: {context.scene.data_file_path}')

        row = layout.row()
        row.operator("visualization.execute_visu",
                     text="Generate visualization", icon="PLAY")


class VISUALIZATION_OT_open_filebrowser(bpy.types.Operator, ImportHelper):

    bl_idname = "visualization.open_filebrowser"
    bl_label = "Select .txt File"
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    filter_glob: bpy.props.StringProperty(default="*.txt", options={'HIDDEN'})

    def invoke(self, context: Context, event: Event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context: Context):
        context.scene.data_file_path = self.properties.filepath
        print(f'Selected file: {self.filepath}')
        return {'FINISHED'}


class VISUALIZATION_OT_generate_visu(bpy.types.Operator):
    bl_idname = "visualization.execute_visu"
    bl_label = "Generate Visualization"

    def execute(self, context: Context):
        if not context.scene.data_file_path:
            self.report(
                {'WARNING'}, "No .txt file selected. Please select a file to visualize.")
            return {'CANCELLED'}

        print('Generating visualization ...')

        self.report(
            {'INFO'}, f'Visualization for {os.path.basename(context.scene.data_file_path)} has been generated successfully.')
        return {'FINISHED'}
