import bpy

from bpy.types import PropertyGroup
from bpy.props import (
    IntProperty,
    FloatProperty,
)


class OBJECT_PT_parameters_section(bpy.types.Panel):
    """
    Class to create a Blender Panel in the VIEW_3D context in the UI region of the screen.
    This panel is labelled 'Global settings' and belongs to the 'CEM' category.
    It is used to configure the global settings of the scene.
    """

    bl_label = 'Global settings'
    bl_idname = 'OBJECT_PT_parameters_section'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CEM'

    @classmethod
    def poll(self, context):
        """
        This method enables the panel only if there is an active object.
        """
        return context.object is not None

    def draw(self, context):
        """
        This method is called when the UI draws the panel.
        It draws the panel UI for configuring the global settings.
        """
        layout = self.layout
        self.draw_parameters_section(context, layout)

    def draw_parameters_section(self, context, layout):
        """
        This method is used to draw the UI components for the global settings section.
        It includes controls for configuring the mesh size and the frequency.
        """
        row = layout.row()
        row.label(text='Global settings', icon='MOD_WAVE')

        # Get the current scene and the global settings from it
        scene = context.scene
        global_settings = scene.settings

        # Draw the controls for configuring the mesh size and the frequency
        # 'layout.prop' automatically creates an interactive UI element for a given property
        layout.prop(global_settings, "mesh_size")
        layout.prop(global_settings, "frequency")
        layout.separator()


class GlobalSettings(PropertyGroup):
    """
    This class represents the global settings of the scene.
    It includes properties for configuring the mesh size and the frequency.
    This is a PropertyGroup which is a way to group related properties together.
    The properties are then accessible in the UI for the user to manipulate.
    """

    # The 'FloatProperty' and 'IntProperty' are a way to define a property
    # that can be edited in the UI and stored with the scene data. They also
    # provide minimum, maximum, and default values.
    mesh_size: FloatProperty(
        name="Mesh size",
        description="Size of the mesh for the voxelization",
        default=.1,
        min=0.001,
        max=1
    )

    frequency: IntProperty(
        name="Frequency",
        description="Frequency",
        default=1
    )
