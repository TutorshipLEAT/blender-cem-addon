# from src.preferences import DependenciesPreferences, DependenciesInstaller
# import bpy
# from src.addon_properties import MaterialProperties, OBJECT_OT_stl_to_msh, OBJECT_PT_material_properties, menu_func


import sys
import subprocess
import trimesh
import seaborn as sns
import matplotlib.pyplot as plt
import bpy
from bpy.types import Panel, Operator, UIList
import os
from mathutils import Vector

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


###### Properties ######

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
    bl_label = "Generate OBJ file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Define file paths
        blend_directory = bpy.path.abspath("//")

        if not os.path.exists(blend_directory):
            self.report({'ERROR'}, "Blend file not saved, Please open an existing blend file or save the current blend file")
            return {'FINISHED'}

            # blend_directory = os.path.expanduser("~")
        stl_file = os.path.join(blend_directory, "export", "object.stl")
        obj_file = os.path.join(blend_directory, "export", "object.obj")
        if not os.path.exists(os.path.join(blend_directory, "export")):
            os.makedirs(os.path.join(blend_directory, "export"))
        # Export the selected objects to an STL file
        export_stl(context, stl_file)

        # Convert the STL file to a .msh file using Gmsh
        stl_to_msh(blend_directory, stl_file, obj_file)

        # Add material properties to the objects
        add_material_properties()

        self.report({'INFO'}, "Conversion to OBJ completed")
        return {'FINISHED'}


###### MAIN UI ######

class OBJECT_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.object.name, icon='OBJECT_DATA')

class FilteredObjectItem(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(type=bpy.types.Object)

def is_inside_cube(obj, cube):
    cube_bounds = [cube.matrix_world @
                   Vector(corner) for corner in cube.bound_box]
    cube_min = Vector((min(v[i] for v in cube_bounds) for i in range(3)))
    cube_max = Vector((max(v[i] for v in cube_bounds) for i in range(3)))

    obj_bounds = [obj.matrix_world @
                  Vector(corner) for corner in obj.bound_box]
    obj_min = Vector((min(v[i] for v in obj_bounds) for i in range(3)))
    obj_max = Vector((max(v[i] for v in obj_bounds) for i in range(3)))

    return all(cube_min[i] <= obj_min[i] and obj_max[i] <= cube_max[i] for i in range(3))


def update_filtered_objects(self, context):
    container_name = "CubeScene"
    container = bpy.data.objects.get(container_name)
    container.display_type = 'WIRE'
    if container:
        objects_inside_cube = [
            obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and is_inside_cube(obj, container)]

        # Update filtered_objects
        filtered_objects = context.scene.FilteredObjects
        filtered_objects.clear()
        for obj in objects_inside_cube:
            if (obj.name == container_name):
                continue
            item = filtered_objects.add()
            item.object = obj

class OBJECT_PT_material_properties(bpy.types.Panel):
    bl_label = 'Converter'
    bl_idname = 'OBJECT_PT_data_load'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Converter'

    def draw(self, context):
        layout = self.layout

        container = bpy.data.objects.get("CubeScene")
        if not container:
            print("CubeScene not found.")
            layout.label(text="CubeScene not found.")
            layout.operator("scene.create_cubescene", text="Create CubeScene")
        else:
            self.draw_scene_section(context, layout)

        self.draw_simulation_section(context, layout)

    def draw_scene_section(self, context, layout):

        row = layout.row()
        row.label(text='Detected Objects', icon='ALIGN_JUSTIFY')

        col = layout.column()
        col.template_list("OBJECT_UL_List", "", context.scene,
                          "FilteredObjects", context.scene, "active_object_index")

        row = layout.row()
        row.operator("scene.update_list", text="Update List")
        row.operator(OBJECT_OT_stl_to_msh.bl_idname,
                     text="Convert Selected to MSH 2")

    def draw_simulation_section(self, context, layout):
        row = layout.row()
        row.label(text='Simulation', icon='MOD_WAVE')





class UpdateListOperator(bpy.types.Operator):
    bl_idname = "scene.update_list"
    bl_label = "Update List Operator"

    def execute(self, context):
        update_filtered_objects(self=None, context=context)
        return {'FINISHED'}


class CreateCubeSceneOperator(bpy.types.Operator):
    bl_idname = "scene.create_cubescene"
    bl_label = "Create CubeScene Operator"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Create a CubeScene object?")

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        cube = context.active_object
        cube.name = "CubeScene"
        cube.display_type = 'WIRE'
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_stl_to_msh.bl_idname)


###### Converters ######

def export_stl(context, filepath):
    # Store the current selection
    current_selected_objects = context.selected_objects

    # Deselect all objectsouf juste à temps ;)

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
        self.mtl_file = os.path.join(self.blender_dir, "materials", mtl_name + ".mtl")

    def export_obj(self, obj_file="export.obj"):
        """
        Exports the voxelized stl file as an obj file.
        """
        boxes = self._voxelize()
        self._save(boxes, obj_file)

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
                boxes, mtl_name=self.mtl_file))

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

def stl_to_msh(blender_dir, stl_file, obj_file):
    """
    Converts a stl file to a msh file.

    Parameters
    ----------
    stl_file : str
        Path to the stl file.
    msh_file : str
        Path to the msh file.
    """
    v = Voxelizer(stl_file, stl_file.split(".stl")[0], blender_dir)
    v.export_obj(obj_file=obj_file)



###### PIP ######


PYPATH = sys.executable


class Pip:

    def __init__(self):
        self._ensurepip()

    @staticmethod
    def _ensure_user_site_package():
        import os
        import site
        import sys
        # site_package = site.getusersitepackages()
        site_package = bpy.utils.user_resource('SCRIPTS', path="site_package")

        if not os.path.exists(site_package):
            site_package = bpy.utils.user_resource(
                'SCRIPTS', path="site_package", create=True)
            site.addsitedir(site_package)
        if site_package not in sys.path:
            sys.path.append(site_package)
    '''
    @staticmethod
    def _ensure_user_site_package():
        import os
        import site
        import sys
        site_package = site.getusersitepackages()
        if os.path.exists(site_package):
            if site_package not in sys.path:
                sys.path.append(site_package)
        else:
            site_package = bpy.utils.user_resource('SCRIPTS', "site_package", create=True)
            site.addsitedir(site_package)
    '''

    def _cmd(self, action, options, module):
        if options is not None and "--user" in options:
            self._ensure_user_site_package()

        cmd = [PYPATH, "-m", "pip", action]

        if options is not None:
            cmd.extend(options.split(" "))

        cmd.append(module)
        return self._run(cmd)

    def _popen(self, cmd):
        popen = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
        popen.stdout.close()
        popen.wait()

    def _run(self, cmd):
        res = False
        status = ""
        for line in self._popen(cmd):
            if "ERROR:" in line:
                status = line.strip()
            if "Error:" in line:
                status = line.strip()
            if "Successfully" in line:
                status = line.strip()
                res = True
        return res, status

    def _ensurepip(self):
        pip_not_found = False
        try:
            import pip
        except ImportError:
            pip_not_found = True
            pass
        if pip_not_found:
            self._run([PYPATH, "-m", "ensurepip", "--default-pip"])

    @staticmethod
    def upgrade_pip():
        import pip
        return pip.main(["install", "--upgrade", "pip"])

    @staticmethod
    def uninstall(module, options=None):
        """
        :param module: string module name with requirements see:[1]
        :param options: string command line options  see:[2]
        :return: True on uninstall, False if already removed, raise on Error
        [1] https://pip.pypa.io/en/stable/reference/pip_install/#id29
        [2] https://pip.pypa.io/en/stable/reference/pip_install/#id47
        """
        import pip

        if options is None or options.strip() == "":
            # force confirm
            options = "-y"
        return pip.main(["uninstall", module, options])

    @staticmethod
    def install(module, options=None):
        """
        :param module: string module name with requirements see:[1]
        :param options: string command line options  see:[2]
        :return: True on install, False if already there, raise on Error
        [1] https://pip.pypa.io/en/stable/reference/pip_install/#id29
        [2] https://pip.pypa.io/en/stable/reference/pip_install/#id47
        """
        import pip
        pip
        return pip.main(["install", module])

    @staticmethod
    def blender_version():
        """
        :return: blender version tuple
        """
        return bpy.app.version

    @staticmethod
    def python_version():
        """
        :return: python version object
        """
        # version.major, version.minor, version.micro
        return sys.version_info

###### Dependencies ######



DEPENDENCIES = ['seaborn', 'trimesh', 'matplotlib']


class DependenciesPreferences(bpy.types.AddonPreferences):
    bl_idname = "mesh_converter"

    def draw(self, context):

        import importlib
        # from src.pip_utils import Pip
        Pip._ensure_user_site_package()

        layout = self.layout
        for dep in DEPENDENCIES:
            if importlib.util.find_spec(dep) is not None:
                layout.label(text=dep + ' loaded.', icon='INFO')
            else:
                layout.label(text="Missing dependencies", icon='ERROR')
                row = layout.row()
                row.operator('blendmsh.installer')
                break


class DependenciesInstaller(bpy.types.Operator):
    bl_idname = "blendmsh.installer"
    bl_label = "Install dependencies"
    bl_description = ("Install dependencies")

    def execute(self, context):
        try:
            self.report({"INFO"}, "Installing dependencies...")
            # from src.pip_utils import Pip
            Pip.upgrade_pip()
            for dep in DEPENDENCIES:
                Pip.install(dep)

            self.report({'INFO'}, 'Dependencies successfully installed.')
        except ModuleNotFoundError:
            self.report({'ERROR'}, 'Could not install dependencies.')
        return {'FINISHED'}

###### Register ######

def register():
    print("Registering...")
    bpy.utils.register_class(DependenciesPreferences)
    bpy.utils.register_class(DependenciesInstaller)
    bpy.utils.register_class(MaterialProperties)
    bpy.utils.register_class(OBJECT_OT_stl_to_msh)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    bpy.types.Object.material_properties = bpy.props.PointerProperty(
        type=MaterialProperties)

    bpy.utils.register_class(FilteredObjectItem)
    bpy.utils.register_class(OBJECT_UL_List)  # list in blender UI +
    bpy.utils.register_class(OBJECT_PT_material_properties)
    # update list when object is added or removed +
    bpy.utils.register_class(UpdateListOperator)
    bpy.utils.register_class(CreateCubeSceneOperator)
    bpy.types.Scene.FilteredObjects = bpy.props.CollectionProperty(
        type=FilteredObjectItem)  # type of list item +
    bpy.types.Scene.active_object_index = bpy.props.IntProperty(
        update=update_filtered_objects)  # index of active item in list +


def unregister():
    bpy.utils.unregister_class(DependenciesPreferences)
    bpy.utils.unregister_class(DependenciesInstaller)
    bpy.utils.unregister_class(MaterialProperties)
    bpy.utils.unregister_class(OBJECT_OT_stl_to_msh)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    del bpy.types.Object.material_properties


    bpy.utils.unregister_class(FilteredObjectItem)
    bpy.utils.unregister_class(OBJECT_UL_List)
    bpy.utils.unregister_class(OBJECT_PT_material_properties)
    bpy.utils.unregister_class(UpdateListOperator)
    bpy.utils.unregister_class(CreateCubeSceneOperator)
    del bpy.types.Scene.FilteredObjects
    del bpy.types.Scene.active_object_index

######## Abstract_plot ##########


Labels = list[str]
Ticks = list[int]


class AbstractPlot:

    def set_legend(self, **kwargs) -> None:
        if ('labels' in kwargs and 'handles' in kwargs):
            plt.legend(labels=kwargs['labels'], handles=kwargs['handles'])
        elif ('labels' in kwargs and not 'handles' in kwargs):
            plt.legend(labels=kwargs['labels'])
        elif (not 'labels' in kwargs and 'handles' in kwargs):
            plt.legend(handles=kwargs['handles'])

    def set_title(self, title: str) -> None:
        plt.title(title)

    def set_xlabel(self, label: str) -> None:
        plt.xlabel(label)

    def set_ylabel(self, label: str) -> None:
        plt.ylabel(label)

    def set_xticks(self, ticks: Ticks):
        plt.xticks(ticks)

    def set_yticks(self, ticks: Ticks):
        plt.yticks(ticks)

    def show(self):
        plt.show()

    def save_to_png(self, path: str) -> None:
        plt.savefig(f'{path}.png')

######## pie_chart ##########


Wedges = list[int]
Labels = list[str]


class PieChart(AbstractPlot):

    def create_pie(self, wedges: Wedges, labels: Labels, autopct: str, colors=None):
        plt.pie(x=wedges, labels=labels, colors=colors, autopct=autopct)

######## bar_chart ##########


class BarChart(AbstractPlot):

    def create_bar(self, bar_position: int, data: list, width: float, bottom=0, align='center', color=None):
        plt.bar(bar_position, data, color=color,
                width=width, bottom=bottom, align=align)


class HeatMap(AbstractPlot):

    def create_heatmap(self, data, annot=False, fmt=".1f", cmap=None, vmin=None, vmax=None, linewidth=.0, linecolor="white"):
        sns.heatmap(data=data, annot=annot, fmt=fmt,
                    cmap=cmap, vmin=vmin, vmax=vmax, linewidth=linewidth, linecolor=linecolor)


if __name__ == "__main__":
    register()
    bpy.context.scene.active_object_index = 0
