import bpy


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
