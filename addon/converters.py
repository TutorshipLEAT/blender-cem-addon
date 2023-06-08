
import bpy
import os
from .constants import VOXELS_DIR
from .voxelizer import Voxelizer, CustomMaterial


class OBJECT_OT_stl_to_msh(bpy.types.Operator):
    bl_idname = "object.stl_to_msh"
    bl_label = "Generate OBJ file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Define file paths
        blend_directory = bpy.path.abspath("//")

        if not os.path.exists(blend_directory):
            self.report(
                {'ERROR'}, "Blend file not saved, Please open an existing blend file or save the current blend file")
            return {'FINISHED'}

        if not os.path.exists(os.path.join(blend_directory, VOXELS_DIR)):
            os.makedirs(os.path.join(blend_directory, VOXELS_DIR))

        filtered_objects = context.scene.FilteredObjects
        global_settings = context.scene.settings
        bpy.ops.object.select_all(action='DESELECT')
        self.report({'INFO'}, "Conversion to OBJ started")
        for obj in filtered_objects:
            current_object = obj.object
            current_object.select_set(True)
            bpy.context.view_layer.objects.active = current_object
            custom_properties = {}
            if current_object.type == 'MESH':
                if len(current_object.keys()) > 2:
                    # First item is _RNA_UI
                    for property in list(current_object.keys())[1:]:
                        if property not in '_RNA_UI':
                            custom_properties[property] = current_object[property]
            self.report({'INFO'}, f"{current_object}")
            stl_file = os.path.join(
                blend_directory, VOXELS_DIR, f"{current_object.name}.stl")
            obj_file = os.path.join(
                blend_directory, VOXELS_DIR, f"{current_object.name}.obj")
            self.report({'INFO'}, f"{stl_file}")
            self.report({'INFO'}, f"{obj_file}")
            bpy.ops.export_mesh.stl(filepath=stl_file, use_selection=True)
            stl_to_msh(global_settings.mesh_size, blend_directory, stl_file, obj_file,
                       CustomMaterial(**custom_properties))
            current_object.select_set(False)
        self.report({'INFO'}, "Conversion to OBJ completed")
        return {'FINISHED'}


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


def stl_to_msh(mesh_size, blender_dir, stl_file, obj_file,
               custom_material: CustomMaterial = None):
    """
    Converts a stl file to a msh file.

    Parameters
    ----------
    stl_file : str
        Path to the stl file.
    msh_file : str
        Path to the msh file.
    """
    v = Voxelizer(stl_file, stl_file.split(".stl")[
                  0], blender_dir, voxel_size=mesh_size)
    v.export_obj(obj_file=obj_file, custom_material=custom_material)
