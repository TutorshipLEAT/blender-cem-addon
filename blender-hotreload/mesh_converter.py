# from src.preferences import DependenciesPreferences, DependenciesInstaller
# import bpy
# from src.addon_properties import MaterialProperties, OBJECT_OT_stl_to_msh, OBJECT_PT_material_properties, menu_func


import bpy
import os

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


###### Converters ######

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
    import gmsh
    gmsh.initialize()
    gmsh.open(stl_file)

    # Set Gmsh options
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 1.0)

    # Set mesh algorithm to Delaunay
    # gmsh.option.setNumber("Mesh.Algorithm", 1)

    # fill the volume with tetrahedra
    gmsh.option.setNumber("Mesh.Algorithm3D", 1)

    # Generate 3D mesh
    gmsh.model.mesh.generate(3)

    # Save the .msh file
    gmsh.write(msh_file)
    gmsh.finalize()


###### PIP ######

import bpy
import subprocess
import sys


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
            print(line)
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

DEPENDENCIES = ['gmsh', 'matplotlib']


class DependenciesPreferences(bpy.types.AddonPreferences):
    bl_idname = "mesh_converter"

    def draw(self, context):

        import importlib
        from src.pip_utils import Pip
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
            print("Installing dependencies...")
            from src.pip_utils import Pip
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
