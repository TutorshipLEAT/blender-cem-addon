
import bpy
import os
from .constants import VOXELS_DIR
from .voxelizer import Voxelizer, CustomMaterial


class OBJECT_OT_stl_to_obj(bpy.types.Operator):
    """
    Operator to convert STL files to MSH format.

    Provides an interface for the user to perform the conversion from the Blender UI.
    """

    bl_idname = "object.stl_to_obj"
    bl_label = "Generate OBJ file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """
        Main execution function which is called when the operator is run.

        Handles the conversion of STL files to MSH.
        """

        blend_directory = bpy.path.abspath("//")

        if not os.path.exists(blend_directory):
            self.report(
                {'ERROR'}, "Blend file not saved, Please open an existing blend file or save the current blend file")
            return {'FINISHED'}

        if not os.path.exists(os.path.join(blend_directory, VOXELS_DIR)):
            os.makedirs(os.path.join(blend_directory, VOXELS_DIR))

        # Filtering objects from the context.
        filtered_objects = context.scene.FilteredObjects

        # Extracting global settings from the context.
        global_settings = context.scene.settings

        # Deselecting all objects to prepare for operation.
        bpy.ops.object.select_all(action='DESELECT')
        self.report({'INFO'}, "Conversion to OBJ started")

        # Looping through the filtered objects
        for obj in filtered_objects:
            current_object = obj.object

            # Selecting the current object and making it active.
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

            # Export the mesh of the current object to an STL file.
            bpy.ops.export_mesh.stl(filepath=stl_file, use_selection=True)

            # Convert the STL file to a OBJ file.
            stl_to_obj(global_settings.mesh_size, blend_directory, stl_file, obj_file,
                       CustomMaterial(**custom_properties))

            # Deselect the current object.
            current_object.select_set(False)
        self.report({'INFO'}, "Conversion to OBJ completed")
        return {'FINISHED'}


def export_stl(context, filepath):
    """
    Export selected mesh objects as STL files.

    This function exports selected mesh objects as STL files, preserving the original selection.

    Parameters
    ----------
    context : bpy.context
        The context provides access to active objects, windows, scenes, etc.
    filepath : str
        The path where the STL file will be saved.
    """

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


def stl_to_obj(mesh_size, blender_dir, stl_file, obj_file,
               custom_material: CustomMaterial = None):
    """
    Converts an STL file to an OBJ file.

    Utilizes the Voxelizer class to perform the conversion.

    Parameters
    ----------
    mesh_size : float
        The mesh size for the voxelization.
    blender_dir : str
        The directory of the Blender file.
    stl_file : str
        The path of the input STL file.
    obj_file : str
        The path of the output OBJ file.
    custom_material : CustomMaterial
        The material properties for the voxelization.
    """

    v = Voxelizer(stl_file, stl_file.split(".stl")[
                  0], blender_dir, voxel_size=mesh_size)
    v.export_obj(obj_file=obj_file, custom_material=custom_material)
