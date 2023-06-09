import trimesh
import os


class CustomMaterial(trimesh.visual.material.Material):
    """
    Custom material for the voxelized mesh.

    Parameters
    ----------
    kwargs : dict
        Keyword arguments for the material.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @property
    def main_color(self):
        return None

    def __hash__(self):
        return hash(self.kwargs)

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

    def export_obj(self, obj_file="export.obj",
                   custom_material: CustomMaterial = None):
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

    def _save(self, boxes, obj_file="export.obj",
              custom_material: CustomMaterial = None):
        self._save_mtl(custom_material)
        self._save_obj(boxes, obj_file)
