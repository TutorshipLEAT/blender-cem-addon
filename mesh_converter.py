from src.preferences import DependenciesPreferences, DependenciesInstaller
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


def register():
    print("Registering...")
    bpy.utils.register_class(DependenciesPreferences)
    bpy.utils.register_class(DependenciesInstaller)
    bpy.utils.register_class(MaterialProperties)
    bpy.utils.register_class(OBJECT_OT_stl_to_msh)
    bpy.utils.register_class(OBJECT_PT_material_properties)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    bpy.types.Object.material_properties = bpy.props.PointerProperty(
        type=MaterialProperties)


def unregister():
    bpy.utils.unregister_class(DependenciesPreferences)
    bpy.utils.unregister_class(DependenciesInstaller)
    bpy.utils.unregister_class(MaterialProperties)
    bpy.utils.unregister_class(OBJECT_OT_stl_to_msh)
    bpy.utils.unregister_class(OBJECT_PT_material_properties)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    del bpy.types.Object.material_properties


if __name__ == "__main__":
    register()
