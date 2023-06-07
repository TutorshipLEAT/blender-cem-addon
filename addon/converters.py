import trimesh
import bpy
import os
from .constants import VOXELS_DIR


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


class CustomMaterial(trimesh.visual.material.Material):
    """
    Custom material for the voxelized mesh.

    Parameters
    ----------
    mtl_name : str
        Name of the material.
    kwargs : dict
        Keyword arguments for the material.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @property
    def main_color(self):
        return None

    def __hash__(self):
        return hash(self.mtl_name)

    def to_obj(self, mtl_file):
        """
        Exports the material as an obj file.

        Parameters
        ----------
        mtl_name : str
            Name of the material.
        """
        mtl_name = os.path.splitext(os.path.basename(mtl_file))[0]
        data = ["newmtl {}".format(mtl_name)]
        for k, v in self.kwargs.items():
            if isinstance(v, int):
                data.append("{} {:0.8f}".format(k, v))
            else:
                data.append("{} {}".format(k, v))
        data = "\n".join(data)
        with open(mtl_file, "w+") as f:
            f.write(data)
        return data


class Voxelizer:
    """
    Voxelizes a stl file and exports it as an obj file.
    """

    def __init__(self, stl_file, mtl_name, blender_dir, voxel_size=.1):
        """
        Parameters
        ----------
        stl_file : str
            Path to the stl file.
        mtl_name : str
            Name of the material.
        voxel_size : float
            Size of the voxels.
        """
        self.stl_file = stl_file
        self.voxel_size = voxel_size
        self.blender_dir = blender_dir
        self.mtl_name = mtl_name
        self.mtl_file = os.path.join(
            self.blender_dir, "materials", mtl_name + ".mtl")

    def export_obj(self, obj_file="export.obj", custom_material: CustomMaterial = None):
        """
        Exports the voxelized stl file as an obj file.
        """
        boxes = self._voxelize()
        self._save(boxes, obj_file, custom_material)

    def _voxelize(self):
        """
        Voxelizes the stl file.

        Returns
        -------
        boxes : trimesh.Trimesh
            Voxelized mesh.
        """
        mesh = trimesh.load(self.stl_file)
        voxelgrid = mesh.voxelized(self.voxel_size)
        return voxelgrid.as_boxes()

    def _save_obj(self, boxes, obj_file="export.obj"):
        """
        Saves the voxelized mesh as an obj file.

        Parameters
        ----------
        boxes : trimesh.Trimesh
            Voxelized mesh.
        obj_file : str
            Path to the obj file.
        """
        with open(obj_file, "w+") as f:
            f.write(trimesh.exchange.obj.export_obj(
                boxes, mtl_name=os.path.abspath(self.mtl_file)))

    def _save_mtl(self, custom_material: None | CustomMaterial = None):
        """
        Saves the material of the voxelized mesh as a mtl file.

        Parameters
        ----------
        custom_material : CustomMaterial
            Custom material.
        """
        if custom_material is None:
            custom_material = CustomMaterial(
                sigma=1, mu=1, epsilon=1, custom_property=.5)
        mtl_data = custom_material.to_obj(self.mtl_file)

        with open(self.mtl_file, "w+") as f:
            f.write(mtl_data)

    def _save(self, boxes, obj_file="export.obj", custom_material: CustomMaterial = None):
        self._save_mtl(custom_material)
        self._save_obj(boxes, obj_file)


def stl_to_msh(mesh_size, blender_dir, stl_file, obj_file, custom_material: CustomMaterial = None):
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
