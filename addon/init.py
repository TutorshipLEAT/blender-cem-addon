import bpy

from bpy.props import (
    IntProperty,
    PointerProperty,
    StringProperty,
    CollectionProperty,
    EnumProperty
)

from . converters import OBJECT_OT_stl_to_msh
from . scene_opt import CreateCubeSceneOperator, FilteredObjectItem, OBJECT_PT_scene_section, OBJECT_UL_List, UpdateListOperator, update_filtered_objects
from . settings_opt import GlobalSettings, OBJECT_PT_parameters_section
from . simulation_opt import OBJECT_PT_simulation_section, SIMULATION_OT_execute_simulation, SIMULATION_OT_open_filebrowser
from . visualization_opt import OBJECT_PT_visualization_section, VISUALIZATION_OT_generate_visu, VISUALIZATION_OT_open_filebrowser


classes = (
    OBJECT_OT_stl_to_msh,
    OBJECT_PT_parameters_section,
    OBJECT_PT_scene_section,
    OBJECT_PT_simulation_section,
    OBJECT_PT_visualization_section,
    OBJECT_UL_List,
    FilteredObjectItem,
    UpdateListOperator,
    CreateCubeSceneOperator,
    GlobalSettings,
    SIMULATION_OT_open_filebrowser,
    SIMULATION_OT_execute_simulation,
    VISUALIZATION_OT_open_filebrowser,
    VISUALIZATION_OT_generate_visu
)


def register_init():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.FilteredObjects = CollectionProperty(
        type=FilteredObjectItem)  # type of list item +
    bpy.types.Scene.active_object_index = IntProperty(
        update=update_filtered_objects)  # index of active item in list +
    bpy.types.Scene.settings = PointerProperty(type=GlobalSettings)
    bpy.types.Scene.obj_file_path = StringProperty(
        name="Obj File Path",
        description="The path of the selected .obj file for simulation",
        default="",
        subtype='FILE_PATH'
    )
    bpy.types.Scene.data_file_path = StringProperty(
        name="Data file path",
        description="The path of the selected .txt file for visualization",
        default="",
        subtype='FILE_PATH'
    )
    bpy.types.Scene.simulation_types = EnumProperty(
        name="Simulation Types",
        description="Choose the type of the simulation",
        items=[
            ('UNIDIMENSIONAL', "Unidimensional", "Unidimensional simulation"),
            ('BIDIMENSIONAL', "Bidimensional", "Bidimensional simulation"),
            ('TRIDIMENSIONAL', "Tridimensional", "Tridimensional simulation"),
        ]
    )
    bpy.types.Scene.visualization_types = EnumProperty(
        name="Visualization types",
        description="Choose the type of visualization",
        items=[
            ('BARPLOT', 'Barplot', 'Barplot visualization'),
            ('HEATMAP', 'Heatmap', 'Heatmap visualization'),
            ('SCATTERPLOT', 'Scatterplot', 'Scatterplot visualization'),
            ('SURFACECHART', 'Surfacechart', 'Surfacechart visualization'),
            ('BUBBLEPLOT', 'Bubbleplot', 'Bubbleplot visualization'),
        ]
    )


def unregister_init():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.FilteredObjects
    del bpy.types.Scene.active_object_index
    del bpy.types.Scene.settings

    del bpy.types.Scene.obj_file_path
    del bpy.types.Scene.simulation_types
    del bpy.types.Scene.data_file_path
    del bpy.types.Scene.visualization_types
