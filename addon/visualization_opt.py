import bpy
import os

from bpy.types import Context, Event
from bpy_extras.io_utils import ImportHelper
from .plot import *
from .constants import VISUALISATIONS_DIR
from .visualisations import *


class OBJECT_PT_visualization_section(bpy.types.Panel):
    """
    The visualization panel in the UI of the blender 3D view.
    """

    bl_label = 'Visualization'
    bl_idname = 'OBJECT_PT_visualization_section'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CEM'

    def draw(self, context):
        """
        Draws the visualization panel.
        """
        layout = self.layout
        self.draw_visualization_section(context, layout)

    def draw_visualization_section(self, context, layout):
        """
        Draw the visualization section on the panel.
        """
        # Add a label and selection properties for visualization types
        row = layout.row()
        row.label(text='Visualization', icon='MOD_WAVE')

        col = layout.column()
        col.prop(context.scene, 'visualization_types', text="")

        # Add button to open file browser for selecting a data file
        row = layout.column()
        row.operator('visualization.open_filebrowser',
                     text="Select .txt File", icon="FILEBROWSER")

        # Show the path of the selected file
        if (context.scene.data_file_path):
            row = layout.row()
            row.label(text=f'Selected file: {context.scene.data_file_path}')

        # Add button to generate visualization
        row = layout.row()
        row.operator("visualization.execute_visu",
                     text="Generate visualization", icon="PLAY")


class VISUALIZATION_OT_open_filebrowser(bpy.types.Operator, ImportHelper):
    """
    An operator for opening the file browser and selecting a data file.
    """
    bl_idname = "visualization.open_filebrowser"
    bl_label = "Select .txt File"
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    filter_glob: bpy.props.StringProperty(
        default="*.txt;*.csv", options={'HIDDEN'})

    def invoke(self, context: Context, event: Event):
        """
        Invokes the file browser.
        """
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context: Context):
        """
        Executes when a file is selected.
        Stores the filepath in the scene properties.
        """
        context.scene.data_file_path = self.properties.filepath
        print(f'Selected file: {self.filepath}')
        return {'FINISHED'}


class VISUALIZATION_OT_generate_visu(bpy.types.Operator):
    """
    An operator for generating a visualization based on the selected data file and visualization type.
    """
    bl_idname = "visualization.execute_visu"
    bl_label = "Generate Visualization"

    def execute(self, context: Context):
        """
        Executes the visualization generation.
        """
        # Check if a data file has been selected
        if not context.scene.data_file_path:
            self.report(
                {'WARNING'}, "No .txt file selected. Please select a file to visualize.")
            return {'CANCELLED'}

        # Define the directory for storing the generated visualizations
        root_dir = bpy.path.abspath("//")
        visusaliation_path = os.path.join(root_dir, VISUALISATIONS_DIR)
        image_path = os.path.join(
            visusaliation_path, context.scene.visualization_types + '.png')

        # If the directory does not exist, create it
        if not os.path.exists(visusaliation_path):
            os.makedirs(visusaliation_path)
            self.report({'INFO'}, f'Created {VISUALISATIONS_DIR} directory')
        self.report({'INFO'}, 'Generating visualization ...')

        # Read data from the selected file and create the corresponding plot
        # Save the plot as a .png image
        # Load the image into Blender and display it in a new image editor area

        if context.scene.visualization_types == 'HEATMAP':
            plot = HeatMap()
            df = read_csv(context.scene.data_file_path)
            plot.create_heatmap([df["x"], df["y"], df["z"]])
            plot.save_to_png(image_path)
        elif context.scene.visualization_types == 'SCATTERPLOT':
            plot = ScatterPlot()
            df = read_csv(context.scene.data_file_path)
            plot.create_scatter(df["x"], df["y"], df["z"])
            plot.save_to_png(image_path)
        elif context.scene.visualization_types == 'SURFACECHART':
            plot = SurfaceChart()
            df = read_csv(context.scene.data_file_path)
            plot.create_surface(df["x"], df["y"], df["z"])
            plot.save_to_png(image_path)
        elif context.scene.visualization_types == 'BUBBLEPLOT':
            plot = BubblePlot()
            df = read_csv(context.scene.data_file_path)
            plot.create_bubble(df["x"], df["y"])
            plot.save_to_png(image_path)

        image = bpy.data.images.load(image_path, check_existing=False)

        # Call user prefs window
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        # Change area type
        area = bpy.context.window_manager.windows[-1].screen.areas[0]
        area.type = 'IMAGE_EDITOR'

        # Assign the image
        bpy.context.area.spaces.active.image = image

        self.report(
            {'INFO'}, f'Visualization for {os.path.basename(context.scene.data_file_path)} has been generated successfully.')
        return {'FINISHED'}
