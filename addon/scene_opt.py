import bpy

from mathutils import Vector
from . converters import OBJECT_OT_stl_to_msh


class OBJECT_PT_scene_section(bpy.types.Panel):
    bl_label = 'Scene'
    bl_idname = 'OBJECT_PT_scene_section'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CEM'

    def draw(self, context):
        layout = self.layout

        container = bpy.data.objects.get("CubeScene")
        if not container:
            print("CubeScene not found.")
            layout.label(text="CubeScene not found.")
            layout.operator("scene.create_cubescene", text="Create CubeScene")
        else:
            self.draw_scene_section(context, layout)

    def draw_scene_section(self, context, layout):

        row = layout.row()
        row.label(text='Detected Objects', icon='ALIGN_JUSTIFY')

        col = layout.column()
        col.template_list("OBJECT_UL_List", "", context.scene,
                          "FilteredObjects", context.scene, "active_object_index")

        row = layout.row()
        row.operator("scene.update_list", text="Update List")
        row.operator(OBJECT_OT_stl_to_msh.bl_idname,
                     text="Convert Selected to MSH")


class OBJECT_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon,
                  active_data, active_propname, index):
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

    return all(cube_min[i] <= obj_min[i] and obj_max[i]
               <= cube_max[i] for i in range(3))


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
