import bpy
import os
from .generate_mesh import export_stl, stl_to_msh

def add_material_properties():
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj["Sigma"] = 1.0
            obj["mu"] = 1.0
            obj["epsilon"] = 1.0


class MaterialProperties(bpy.types.PropertyGroup):
    sigma: bpy.props.FloatProperty(name="Sigma", default=1.0)
    mu: bpy.props.FloatProperty(name="mu", default=1.0)
    epsilon: bpy.props.FloatProperty(name="epsilon", default=1.0)


class OBJECT_OT_stl_to_msh(bpy.types.Operator):
    bl_idname = "object.stl_to_msh"
    bl_label = "Convert to MSH"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Define file paths
        blend_directory = bpy.path.abspath("//")
        if not os.path.exists(blend_directory):
            blend_directory = os.path.expanduser("~")
        stl_file = os.path.join(blend_directory, "object.stl")
        msh_file = os.path.join(blend_directory, "object.msh")

        # Export the selected objects to an STL file
        export_stl(context, stl_file)

        # Convert the STL file to a .msh file using Gmsh
        stl_to_msh(stl_file, msh_file)

        # Add material properties to the objects
        add_material_properties()

        self.report({'INFO'}, "Conversion to MSH completed")
        return {'FINISHED'}


class OBJECT_PT_material_properties(bpy.types.Panel):
    bl_label = "Material Properties"
    bl_idname = "OBJECT_PT_material_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        material_props = obj.material_properties

        row = layout.row()
        row.prop(material_props, 'sigma', text="Sigma")
        row = layout.row()
        row.prop(material_props, 'mu', text="mu")
        row = layout.row()
        row.prop(material_props, 'epsilon', text="epsilon")

        layout.separator()

        row = layout.row()
        row.operator(OBJECT_OT_stl_to_msh.bl_idname,
                     text="Convert Selected to MSH")

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_stl_to_msh.bl_idname)