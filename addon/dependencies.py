import bpy

from . pip_utils import Pip

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
