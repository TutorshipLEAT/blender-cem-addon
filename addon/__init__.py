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

from .constants import DEPENDENCIES

# Metadata about the addon.
bl_info = {
    "name": "CEM LEAT Addon",
    "author": "Tutorship LEAT",
    "version": (1, 0),
    "blender": (3, 3, 5),
    "location": "View3D > Object",
    "description": "Converts a mesh to voxels and visualizes them with a simulation",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}


def register():
    """
    Function to register the addon.

    It attempts to install any missing dependencies from the DEPENDENCIES list defined in 'constants.py'.
    Then it calls the register_init function from the '__init__.py' file.
    """

    try:
        # install dependencies
        import importlib
        import pip
        for dep in DEPENDENCIES:
            if importlib.util.find_spec(dep) is None:
                pip.main(["install", dep])
    except BaseException:
        pass

    # Import and call the register function from the 'init' file
    from . init import register_init
    register_init()


def unregister():
    """
    Function to unregister the addon.

    It calls the unregister_init function from the '__init__.py' file.
    """

    from . init import unregister_init
    unregister_init()
