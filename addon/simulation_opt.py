import bpy
import os

from bpy_extras.io_utils import ImportHelper


class OBJECT_PT_simulation_section(bpy.types.Panel):
    bl_label = 'Simulation'
    bl_idname = 'OBJECT_PT_simulation_section'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CEM'

    def draw(self, context):
        layout = self.layout
        self.draw_simulation_section(context, layout)

    def draw_simulation_section(self, context, layout):
        row = layout.row()
        row.label(text='Simulation type', icon='MOD_WAVE')
        
        col = layout.column()
        col.prop(context.scene, 'simulation_types', text="")

        row = layout.column()
        row.operator('simulation.open_filebrowser', text="Select .obj File", icon='FILEBROWSER')
        
        if (context.scene.obj_file_path):
            row = layout.row()
            row.label(text=f'Selected file: {context.scene.obj_file_path}')
        
        row = layout.row()
        row.operator('simulation.run_simulation', text="Run Simulation", icon='PLAY')


class SIMULATION_OT_open_filebrowser(bpy.types.Operator, ImportHelper):
    bl_idname = "simulation.open_filebrowser"
    bl_label = "Select .obj File"
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")  # Define this to get 'filepath' property to work correctly.

    filter_glob: bpy.props.StringProperty(default="*.obj", options={'HIDDEN'})

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        context.scene.obj_file_path = self.properties.filepath
        print(f'Selected file: {self.filepath}')
        return {'FINISHED'}


class SIMULATION_OT_execute_simulation(bpy.types.Operator):
    bl_idname = "simulation.run_simulation"
    bl_label = "Run Simulation"

    def execute(self, context):
        if not context.scene.obj_file_path:  # If no file is selected
            self.report({'WARNING'}, "No .obj file selected. Please select a file to simulate.")
            return {'CANCELLED'}
        
        # Add simulation execution code here
        print(f'Simulating: {context.scene.obj_file_path}') 

        self.report({'INFO'}, f'Simulation on {os.path.basename(context.scene.obj_file_path)} completed successfully.')
        return {'FINISHED'}
