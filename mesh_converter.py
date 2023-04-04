# from src.preferences import BlendmshPreferences, BlendmshInstaller
import bpy
from src.addon_properties import MaterialProperties, OBJECT_OT_stl_to_msh, OBJECT_PT_material_properties, menu_func

bl_info = {
    "name": "STL to MSH Converter",
    "author": "Tutorship LEAT",
    "version": (1, 0),
    "blender": (3, 3, 5),
    "location": "View3D > Object",
    "description": "Converts selected objects to an STL file and discretizes it using Gmsh",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

class BlendmshPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):

        import importlib
        from src.pip_utils import Pip
        Pip._ensure_user_site_package()

        layout = self.layout
        if importlib.util.find_spec('gmsh') is not None:
            layout.label(text='gmsh loaded.', icon='INFO')
        else:
            layout.label(text='Blendmsh requires gmsh!', icon='ERROR')
            row = layout.row()
            row.operator('blendmsh.installer')

class BlendmshInstaller(bpy.types.Operator):
    bl_idname = "blendmsh.installer"
    bl_label = "Install gmsh"
    bl_description = ("Install gmsh")

    def execute(self, context):
        try:
            print("Installing gmsh...")
            import importlib

            print(importlib.util.find_spec('gmsh'))

            from src.pip_utils import Pip
            Pip.upgrade_pip()
            Pip.install('gmsh')

            import gmsh
            print(gmsh.__version__)
            self.report({'INFO'}, 'Successfully installed gmsh.')
        except ModuleNotFoundError:
            self.report({'ERROR'}, 'Could not install gmsh, Kindly install it manually.')
        return {'FINISHED'}


def register():
    print("Registering...")
    import importlib
    print(importlib.util.find_spec('gmsh'))
    bpy.utils.register_class(BlendmshPreferences)
    bpy.utils.register_class(BlendmshInstaller)
    bpy.utils.register_class(MaterialProperties)
    bpy.utils.register_class(OBJECT_OT_stl_to_msh)
    bpy.utils.register_class(OBJECT_PT_material_properties)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    bpy.types.Object.material_properties = bpy.props.PointerProperty(
        type=MaterialProperties)


def unregister():
    bpy.utils.unregister_class(BlendmshPreferences)
    bpy.utils.unregister_class(BlendmshInstaller)
    bpy.utils.unregister_class(MaterialProperties)
    bpy.utils.unregister_class(OBJECT_OT_stl_to_msh)
    bpy.utils.unregister_class(OBJECT_PT_material_properties)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    del bpy.types.Object.material_properties


if __name__ == "__main__":
    register()
