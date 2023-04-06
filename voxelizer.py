import trimesh
from trimesh.exchange.obj import export_obj
class CustomMaterial(trimesh.visual.material.Material):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @property
    def main_color(self):
        return None

    def __hash__(self):
        return hash(self.mtl_name)

    def to_obj(self, mtl_name):
        data = ["newmtl {}".format(mtl_name)]
        for k, v in self.kwargs.items():
            data.append("{} {:0.8f}".format(k, v))
        data = "\n".join(data)
        with open("{}.mtl".format(mtl_name), "w+") as f:
            f.write(data)
        return data

mesh = trimesh.load('untitled.stl')

my_material = CustomMaterial(sigma=1, mu=1, epsilon=1, custom_property=.5)
trimesh.visual = my_material


voxelgrid = mesh.voxelized(0.1)
boxes = voxelgrid.as_boxes()

mtl_filename = "my_material"
mtl_data = my_material.to_obj(mtl_filename)

with open(f"{mtl_filename}.mtl", "w+") as f:
    f.write(mtl_data)

with open("untitled.obj", "w+") as f:
    f.write(trimesh.exchange.obj.export_obj(boxes, mtl_name=mtl_filename + ".mtl"))


