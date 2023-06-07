import bpy

from bpy.types import PropertyGroup
from bpy.props import (
    IntProperty,
    FloatProperty,
)


class OBJECT_PT_parameters_section(bpy.types.Panel):
    bl_label = 'Global settings'
    bl_idname = 'OBJECT_PT_parameters_section'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CEM'

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        self.draw_parameters_section(context, layout)

    def draw_parameters_section(self, context, layout):
        row = layout.row()
        row.label(text='Global settings', icon='MOD_WAVE')

        scene = context.scene
        global_settings = scene.settings

        layout.prop(global_settings, "mesh_size")
        layout.prop(global_settings, "frequency")
        layout.separator()


class GlobalSettings(PropertyGroup):

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
