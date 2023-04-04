import bpy

class BlendmshPreferences(bpy.types.AddonPreferences):
    bl_idname = "BlendmshPreferences"

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
    print(__name__)
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