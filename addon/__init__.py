# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

from bpy.props import (
    IntProperty,
    PointerProperty,
    StringProperty,
    CollectionProperty,
    EnumProperty
)

# from . converters import OBJECT_OT_stl_to_msh
from . dependencies import DependenciesInstaller, DependenciesPreferences
# from . scene_opt import CreateCubeSceneOperator, FilteredObjectItem, OBJECT_PT_scene_section, OBJECT_UL_List, UpdateListOperator, update_filtered_objects
# from . settings_opt import GlobalSettings, OBJECT_PT_parameters_section
# from . simulation_opt import OBJECT_PT_simulation_section, SIMULATION_OT_execute_simulation, SIMULATION_OT_open_filebrowser
# from . visualization_opt import OBJECT_PT_visualization_section, VISUALIZATION_OT_generate_visu, VISUALIZATION_OT_open_filebrowser


bl_info = {
    "name": "CEM LEAT Addon",
    "author": "Tutorship LEAT",
    "version": (1, 0),
    "blender": (3, 3, 5),
    "location": "View3D > Object",
    "description": "Converts selected objects to an STL file and discretizes it using Gmsh",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}


classes = (
    DependenciesPreferences,
    DependenciesInstaller
    # OBJECT_OT_stl_to_msh,
    # OBJECT_PT_parameters_section,
    # OBJECT_PT_scene_section,
    # OBJECT_PT_simulation_section,
    # OBJECT_PT_visualization_section,
    # OBJECT_UL_List,
    # FilteredObjectItem,
    # UpdateListOperator,
    # CreateCubeSceneOperator,
    # GlobalSettings,
    # SIMULATION_OT_open_filebrowser,
    # SIMULATION_OT_execute_simulation,
    # VISUALIZATION_OT_open_filebrowser,
    # VISUALIZATION_OT_generate_visu
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # bpy.types.Scene.FilteredObjects = CollectionProperty(
    #     type=FilteredObjectItem)  # type of list item +
    # bpy.types.Scene.active_object_index = IntProperty(
    #     update=update_filtered_objects)  # index of active item in list +
    # bpy.types.Scene.settings = PointerProperty(type=GlobalSettings)
    # bpy.types.Scene.obj_file_path = StringProperty(
    #     name="Obj File Path",
    #     description="The path of the selected .obj file for simulation",
    #     default="",
    #     subtype='FILE_PATH'
    # )
    # bpy.types.Scene.data_file_path = StringProperty(
    #     name="Data file path",
    #     description="The path of the selected .txt file for visualization",
    #     default="",
    #     subtype='FILE_PATH'
    # )
    # bpy.types.Scene.simulation_types = EnumProperty(
    #     name="Simulation Types",
    #     description="Choose the type of the simulation",
    #     items=[
    #         ('UNIDIMENSIONAL', "Unidimensional", "Unidimensional simulation"),
    #         ('BIDIMENSIONAL', "Bidimensional", "Bidimensional simulation"),
    #         ('TRIDIMENSIONAL', "Tridimensional", "Tridimensional simulation"),
    #     ]
    # )
    # bpy.types.Scene.visualization_types = EnumProperty(
    #     name="Visualization types",
    #     description="Choose the type of visualization",
    #     items=[
    #         ('BARPLOT', 'Barplot', 'Barplot visualization'),
    #         ('HEATMAP', 'Heatmap', 'Heatmap visualization'),
    #         ('BUBBLECHART', 'Bubblechart', 'Bubblechart visualization'),
    #         ('SCATTERPLOT', 'Scatterplot', 'Scatterplot visualization'),
    #     ]
    # )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # del bpy.types.Scene.FilteredObjects
    # del bpy.types.Scene.active_object_index
    # del bpy.types.Scene.settings

    # del bpy.types.Scene.obj_file_path
    # del bpy.types.Scene.simulation_types
    # del bpy.types.Scene.data_file_path
    # del bpy.types.Scene.visualization_types
