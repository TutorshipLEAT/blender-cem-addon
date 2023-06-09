# blender-cem-addon

Addon to convert object in the scene in voxels. Simulate and visualize stuff around.

![Example addon](./docs/example_addon.png)

## Requierments

Install Blender from the [Official Website](https://www.blender.org/download/) the version 3.3 or above.

> - For Linux, please do not use any packet manager, install it from the source `tar.gz`
> - For MacOS and Windows use the official installer

## First install

This section is a *step-by-step* guide for installing the addon in order to contribute to the project.

### Configure Workspace

In order to develop the add-on, you should use VSCode. You can install the extension [Blender Development](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development) to have a better experience.

Once you have installed the extension, you can open the

1. Start Blender

![Example addon](./docs/blender_extension.png)

2. Select the blender application

![Example addon](./docs/select_blender.png)

Now Blender is open in development mode.

3. You can now see the console and the python editor to debug the add-on easily.

![Example addon](./docs/blender_open.png)
## Dependencies

Now that you've installed the add-ons you can install the dependecies. Dependecies are register in the [constant.py](./addon/constants.py) file. You can add dependencies by adding new item to this list :

```py
DEPENDENCIES = ['seaborn', 'trimesh', 'matplotlib', 'pandas', 'numpy', 'scipy']
```

## Documentation

## Use the add-on