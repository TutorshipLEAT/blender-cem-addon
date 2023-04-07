# blender-cem-addon

Addon to convert object in the scene in voxels. Simulate and visualize stuff around.

## Requierments 

Install Blender from the [Official Website](https://www.blender.org/download/) the version 3.3 or above.

> - For Linux, please do not use any packet manager, install it from the source `tar.gz`
> - For MacOS and Windows use the official installer

## First install

This section is a *step-by-step* guide for installing the addon in order to contribute to the project. This work is still in progress, the workflow will not stay as it is right now.

### Install dependencies

Before any steps, you can install dependencies by installing the addon using the python console of blender. In the console type :

```py
import pip
pip.main(["install", "trimesh", "matplotlib", "seaborn"])
```

<img src="/docs/pip.png" width="600px" height="auto">

Now that you've installed the add-ons you can install the dependecies. Dependecies are register in the [mesh_converter.py](/blender-hotreload/mesh_converter.py). You can add dependencies by adding new item to this list : 

```py
485   DEPENDENCIES = ['seaborn', 'trimesh', 'matplotlib']
```

Once you've imported the script you must activate the add-on by checking the check-box of the add-on, and click on the **Install dependencies**'s button as show the following screen : 

<img src="/docs/dependencies.png" alt= “” width="600px" height="auto">

### Configure Workspace

In order to develop the add-on, you should use the scripting tab and load the [mesh_converter.py](/blender-hotreload/mesh_converter.py) in the text editor. Here you can write code and rerun the code in order to develop new features. 

![](/docs/scripting_workspace.png)


## Documentation

### Use the add-on 

![](/docs/use.png)

In order to convert the objects in voxels, you have to create the **CubeScene** in the panel of the add-on. Once you've created the cube, you can scale it and move it in the viewport. By moving other object in the scene, if you place objects inside the **CubeScene** you can click on the update list button. Then you can convert the selected files. *WORK IN PROGRESS*

You can browse the code to find the class `Voxelizer` in [mesh_converter.py](/blender-hotreload/mesh_converter.py). You can modify this class to try other options of voxelisation. 
