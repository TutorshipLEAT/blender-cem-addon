import bpy
import os

from bpy_extras.io_utils import ImportHelper
from .constants import SIMULATIONS_DIR
from .simulations import run_simulation


class OBJECT_PT_simulation_section(bpy.types.Panel):
    """
    Panel for the Simulation section in the UI.

    It contains the logic to draw UI elements, and react to user input.
    """

    bl_label = 'Simulation'
    bl_idname = 'OBJECT_PT_simulation_section'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CEM'

    def draw(self, context):
        layout = self.layout
        self.draw_simulation_section(context, layout)

    def draw_simulation_section(self, context, layout):
        """ Draw the Simulation section in the UI """

        # Handles UI element placement for simulation selection and file
        # selection.
        row = layout.row()
        row.label(text='Simulation type', icon='MOD_WAVE')

        row = layout.column()
        row.operator(
            'simulation.open_filebrowser',
            text="Select .obj File",
            icon='FILEBROWSER')

        # Checks if a file is selected and handles the UI display for it.
        if (context.scene.obj_file_path and os.path.isfile(
                context.scene.obj_file_path)):
            row = layout.row()
            row.label(text=f'Selected file: {context.scene.obj_file_path}')

            col = layout.column()
            col.prop(context.scene, 'simulation_types', text="")

            row = layout.row()
            row.operator(
                'simulation.run_simulation',
                text="Run Simulation",
                icon='PLAY')
        else:
            row = layout.row()
            row.label(text=f'No file selected.')


class SIMULATION_OT_open_filebrowser(bpy.types.Operator, ImportHelper):
    """
    Operator to handle the action of opening a file browser.

    Uses the ImportHelper mixin to facilitate file handling.
    """

    bl_idname = "simulation.open_filebrowser"
    bl_label = "Select .obj File"
    # filepath prop to store the user-selected file path.
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    filter_glob: bpy.props.StringProperty(default="*.obj", options={'HIDDEN'})

    def invoke(self, context, event):
        """ Opens the file browser."""

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        """ Sets the filepath to the user selected file path. """

        context.scene.obj_file_path = self.properties.filepath
        print(f'Selected file: {self.filepath}')
        return {'FINISHED'}


class SIMULATION_OT_execute_simulation(bpy.types.Operator):
    """ Operator to handle the action of running the simulation. """

    bl_idname = "simulation.run_simulation"
    bl_label = "Run Simulation"

    def execute(self, context):
        """ Runs the simulation """

        blend_directory = bpy.path.abspath("//")

        # Creates a simulations directory if it doesn't exist.
        if not os.path.exists(blend_directory):
            self.report(
                {'ERROR'}, "Blend file not saved, Please open an existing blend file or save the current blend file")
            return {'FINISHED'}

        # Checks if a file is selected for simulation.
        if not os.path.exists(os.path.join(blend_directory, SIMULATIONS_DIR)):
            os.makedirs(os.path.join(blend_directory, SIMULATIONS_DIR))

        if not context.scene.obj_file_path:  # If no file is selected
            self.report(
                {'WARNING'},
                "No .obj file selected. Please select a file to simulate.")
            return {'CANCELLED'}

        # Add simulation execution code here
        print(f'Simulating: {context.scene.obj_file_path}')
        save_path = os.path.join(blend_directory, SIMULATIONS_DIR)

        # Executes the appropriate simulation based on user selection.
        if (context.scene.simulation_types == 'UNIDIMENSIONAL'):
            run_simulation(1, context, context.scene.obj_file_path, save_path)

        elif (context.scene.simulation_types == 'BIDIMENSIONAL'):
            run_simulation(2, context, context.scene.obj_file_path, save_path)

        elif (context.scene.simulation_types == 'TRIDIMENSIONAL'):
            run_simulation(3, context, context.scene.obj_file_path, save_path)

        else:
            self.report(
                {'ERROR'},
                "Invalid simulation type. Please select a valid simulation type.")
            return {'CANCELLED'}

        self.report(
            {'INFO'},
            f'Simulation on {os.path.basename(context.scene.obj_file_path)} completed successfully. Files saved to {save_path}')
        return {'FINISHED'}
