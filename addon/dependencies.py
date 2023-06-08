import bpy


DEPENDENCIES = ['seaborn', 'trimesh', 'matplotlib', 'pandas', 'numpy']


class DependenciesPreferences(bpy.types.AddonPreferences):
    bl_idname = "addon.dependencies.cem_leat"
    
    def draw(self, context):
        print('draw dependencies preferences')
        import importlib
        from . pip_utils import Pip

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
            
            from . pip_utils import Pip

            Pip.upgrade_pip()
            Pip.install(*DEPENDENCIES)

            self.report({'INFO'}, 'Dependencies successfully installed.')
        except ModuleNotFoundError:
            self.report({'ERROR'}, 'Could not install dependencies.')
        return {'FINISHED'}
