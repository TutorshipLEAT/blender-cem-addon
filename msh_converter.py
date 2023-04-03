bl_info = {
    "name": "STL to MSH Converter",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 3, 5),
    "location": "View3D > Object",
    "description": "Converts selected objects to an STL file and discretizes it using Gmsh",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy
import os
import gmsh

    


def export_stl(context, filepath):
    # Store the current selection
    current_selected_objects = context.selected_objects

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select only the mesh objects and export them
    for obj in current_selected_objects:
        if obj.type == 'MESH':
            obj.select_set(True)
            context.view_layer.objects.active = obj
            bpy.ops.export_mesh.stl(filepath=filepath, use_selection=True)
            obj.select_set(False)

    # Restore the original selection
    for obj in current_selected_objects:
        obj.select_set(True)



def stl_to_msh(stl_file, msh_file):
    gmsh.initialize()
    gmsh.open(stl_file)

    # Set Gmsh options
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 1.0)

    # Set mesh algorithm to Delaunay
    gmsh.option.setNumber("Mesh.Algorithm", 1)

    # # Generate 2D mesh
    # gmsh.model.mesh.generate(2)

    # Generate 3D mesh
    gmsh.model.mesh.generate(3)

    # Save the .msh file
    gmsh.write(msh_file)
    gmsh.finalize()



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
        row.operator(OBJECT_OT_stl_to_msh.bl_idname, text="Convert Selected to MSH")



def menu_func(self, context):
    self.layout.operator(OBJECT_OT_stl_to_msh.bl_idname)

def register():
    bpy.utils.register_class(MaterialProperties)
    bpy.utils.register_class(OBJECT_OT_stl_to_msh)
    bpy.utils.register_class(OBJECT_PT_material_properties)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    bpy.types.Object.material_properties = bpy.props.PointerProperty(type=MaterialProperties)

def unregister():
    bpy.utils.unregister_class(MaterialProperties)
    bpy.utils.unregister_class(OBJECT_OT_stl_to_msh)
    bpy.utils.unregister_class(OBJECT_PT_material_properties)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    del bpy.types.Object.material_properties

