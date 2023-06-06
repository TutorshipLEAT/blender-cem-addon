import bpy


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