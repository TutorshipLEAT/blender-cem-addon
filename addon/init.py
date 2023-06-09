import bpy

from bpy.props import (
    IntProperty,
    PointerProperty,
    StringProperty,
    CollectionProperty,
    EnumProperty
)

# These are the import statements for all the components, operators,
# panels, and other elements of the addon.
from . converters import OBJECT_OT_stl_to_obj
from . scene_opt import CreateCubeSceneOperator, FilteredObjectItem, OBJECT_PT_scene_section, OBJECT_UL_List, UpdateListOperator, update_filtered_objects
from . settings_opt import GlobalSettings, OBJECT_PT_parameters_section
from . simulation_opt import OBJECT_PT_simulation_section, SIMULATION_OT_execute_simulation, SIMULATION_OT_open_filebrowser
from . visualization_opt import OBJECT_PT_visualization_section, VISUALIZATION_OT_generate_visu, VISUALIZATION_OT_open_filebrowser


# All the classes that will be registered to Blender are grouped in this tuple.
classes = (
    OBJECT_OT_stl_to_obj,
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

# Function to register all the classes and properties to Blender.


def register_init():
    # Here it loops over each class in the 'classes' tuple and registers it to
    # Blender.
    for cls in classes:
        bpy.utils.register_class(cls)

    # Here it registers properties to the 'Scene' type in Blender. These properties will be available in every scene.
        # CollectionProperty is used to create a list of custom items
        # (FilteredObjectItem).
    bpy.types.Scene.FilteredObjects = CollectionProperty(
        type=FilteredObjectItem)

    # IntProperty is used to store the index of the active item in the list.
    # When this property is changed, the function 'update_filtered_objects'
    # will be called.
    bpy.types.Scene.active_object_index = IntProperty(
        update=update_filtered_objects)

    # PointerProperty is used to link to the 'GlobalSettings' class, which is
    # used to store global settings for the addon.
    bpy.types.Scene.settings = PointerProperty(type=GlobalSettings)

    # StringProperty is used to store paths to selected files. 'subtype' is
    # set to 'FILE_PATH' to open a file browser when these properties are
    # clicked in the UI.
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

    # EnumProperty is used to create a drop-down menu in the UI. The 'items'
    # parameter is a list of tuples. Each tuple defines one item in the
    # drop-down menu.
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
            ('HEATMAP', 'Heatmap', 'Heatmap visualization'),
            ('SCATTERPLOT', 'Scatterplot', 'Scatterplot visualization'),
            ('SURFACECHART', 'Surfacechart', 'Surfacechart visualization'),
            ('BUBBLEPLOT', 'Bubbleplot', 'Bubbleplot visualization'),
        ]
    )

# Function to unregister all the classes and properties from Blender.


def unregister_init():
    # It loops over each class in the 'classes' tuple and unregisters it from
    # Blender.
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # It deletes the custom properties from the 'Scene' type.
    del bpy.types.Scene.FilteredObjects
    del bpy.types.Scene.active_object_index
    del bpy.types.Scene.settings

    del bpy.types.Scene.obj_file_path
    del bpy.types.Scene.simulation_types
    del bpy.types.Scene.data_file_path
    del bpy.types.Scene.visualization_types
