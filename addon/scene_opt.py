import bpy

from mathutils import Vector
from . converters import OBJECT_OT_stl_to_msh


class OBJECT_PT_scene_section(bpy.types.Panel):
    """
    Class to create a Blender Panel that appears in the VIEW_3D context in the UI region of the screen.
    This panel is labelled 'Scene' and belongs to the 'CEM' category.
    """

    bl_label = 'Scene'
    bl_idname = 'OBJECT_PT_scene_section'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CEM'

    def draw(self, context):
        """
        The draw function is called when the UI draws the panel.
        It checks if the CubeScene object exists. If it doesn't, it offers the user the option to create it.
        If it does exist, it proceeds to draw the rest of the panel UI.
        """
        layout = self.layout

        # Attempt to get a reference to the CubeScene object
        container = bpy.data.objects.get("CubeScene")

        # If the CubeScene object does not exist, offer to create it
        if not container:
            print("CubeScene not found.")
            layout.label(text="CubeScene not found.")
            layout.operator("scene.create_cubescene", text="Create CubeScene")

        # If the CubeScene object does exist, draw the rest of the panel UI
        else:
            self.draw_scene_section(context, layout)

    def draw_scene_section(self, context, layout):
        """
        Function to draw the UI components for the scene section.
        It lists detected objects and provides buttons to update the list and convert selected items to MSH format.
        """

        # Create a new row in the UI layout and label it as 'Detected Objects'
        row = layout.row()
        row.label(text='Detected Objects', icon='ALIGN_JUSTIFY')

        # Create a new column in the layout, in this column, a template list is created, which is essentially a UI list.
        # The list is connected to the 'FilteredObjects' property of the current scene.
        # The active object index of the current scene is used to manage which
        # item in the list is selected.
        col = layout.column()
        col.template_list("OBJECT_UL_List", "", context.scene,
                          "FilteredObjects", context.scene, "active_object_index")

        # Create a new row in the layout with two buttons - one to update the
        # list and the other to convert the selected items to MSH format
        row = layout.row()
        row.operator("scene.update_list", text="Update List")
        row.operator(OBJECT_OT_stl_to_msh.bl_idname,
                     text="Convert Selected to MSH")


class OBJECT_UL_List(bpy.types.UIList):
    """
    UIList is a class to manage drawing a list of items in the UI.
    This class overrides the draw_item function to customize how each item in the list is drawn.
    """

    def draw_item(self, context, layout, data, item, icon,
                  active_data, active_propname, index):
        # Draw each item in the list as a label with the name of the object
        layout.label(text=item.object.name, icon='OBJECT_DATA')


class FilteredObjectItem(bpy.types.PropertyGroup):
    """
    Custom PropertyGroup to hold a reference to an object.
    """

    object: bpy.props.PointerProperty(type=bpy.types.Object)


# Function to check if a 3D object is inside a cube
def is_inside_cube(obj, cube):
    # Compute the world space coordinates of the corners of the bounding box
    # of the cube
    cube_bounds = [cube.matrix_world @
                   Vector(corner) for corner in cube.bound_box]
    # Compute the minimum and maximum coordinates of the bounding box in each
    # dimension
    cube_min = Vector((min(v[i] for v in cube_bounds) for i in range(3)))
    cube_max = Vector((max(v[i] for v in cube_bounds) for i in range(3)))

    # Do the same for the object
    obj_bounds = [obj.matrix_world @
                  Vector(corner) for corner in obj.bound_box]
    obj_min = Vector((min(v[i] for v in obj_bounds) for i in range(3)))
    obj_max = Vector((max(v[i] for v in obj_bounds) for i in range(3)))

    # Check if the bounding box of the object is entirely within the bounding
    # box of the cube
    return all(cube_min[i] <= obj_min[i] and obj_max[i]
               <= cube_max[i] for i in range(3))


# Function to update the list of objects that are inside the CubeScene
def update_filtered_objects(self, context):
    container_name = "CubeScene"
    container = bpy.data.objects.get(container_name)
    container.display_type = 'WIRE'
    if container:
        # Create a list of all the mesh objects in the scene that are inside
        # the cube
        objects_inside_cube = [
            obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and is_inside_cube(obj, container)]

        # Get the list of filtered objects from the current scene and clear it
        filtered_objects = context.scene.FilteredObjects
        filtered_objects.clear()

        # Add each object inside the cube to the list of filtered objects,
        # excluding the cube itself
        for obj in objects_inside_cube:
            if (obj.name == container_name):
                continue
            item = filtered_objects.add()
            item.object = obj


class UpdateListOperator(bpy.types.Operator):
    """
    Operator to call the update_filtered_objects function when clicked in the UI.
    """

    bl_idname = "scene.update_list"
    bl_label = "Update List Operator"

    def execute(self, context):
        update_filtered_objects(self=None, context=context)
        return {'FINISHED'}


class CreateCubeSceneOperator(bpy.types.Operator):
    """
    Operator to create a CubeScene object when clicked in the UI.
    It shows a confirmation dialog before creation.
    """

    bl_idname = "scene.create_cubescene"
    bl_label = "Create CubeScene Operator"

    def invoke(self, context, event):
        # Invoke a dialog to confirm creation of the CubeScene object
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        # Draw the dialog to confirm creation of the CubeScene object
        layout = self.layout
        layout.label(text="Create a CubeScene object?")

    def execute(self, context):
        # Create a new cube primitive, rename it to 'CubeScene', and set it to
        # display as wireframe
        bpy.ops.mesh.primitive_cube_add()
        cube = context.active_object
        cube.name = "CubeScene"
        cube.display_type = 'WIRE'
        return {'FINISHED'}
