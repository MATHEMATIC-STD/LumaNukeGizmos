## menu.py and init.py
Auto creation of menu items for Gizmos. Just drag and drop gizmos into the right folder and they will show up in your Nuke menus. No longer will you have to create the menu items manually for each gizmo you want to install.


## Filter
**ALPHACLEAN**
AlphaClean removes stray pixels from the alpha channel of your matte. Removes black pixels in the white area of the matte and white pixels in the black area.

**BLURHUE**
Blurs just color information on the image. Works well to reduce issues with noisy keys.

**CAMERABLUR**
Use this node to add camera motion blur to an element. Camera should be a rotation only camera. In most cases you can quickly use NukeX's camera tracker to solve a rotation only camera for you and use this.

**EXPONBLUR**
The ExponBlur blurs an image with an exponential falloff based upon an alpha. Most often used with roto shapes. The effect is applied to RGBA only.

## Draw
**ASPECTMASK**
Applies an aspect mask over the image. The mask should properly adjust for image resolution and pixel aspect.

**GRAIN**
Added functionality to Nuke's default grain node.

**SPOT REMOVER**
SpotRemover works similar to MarkerRemoval. This node however blends pixels from areas outside the control matte (alpha) with a smoother feel and does it much faster. It also allows you to control how many pixels surrounding the fill area you use to generate the fill area. There is also independent height and with controls for generating the fill area and the option to control the angle like a directional blur.

## Merge
**FUSE**
Fuse is a replacement for the merge(over) node. Functions for light wrap and hue wrap onto the foreground.

**ICOLOR**
Icolor will apply the hue information from the A input to the B input.

**SWITCHMATTE**
Grabs the alpha channel from the A input and premultiplies it to the B input.

## Keyer
**DESPILL**
A gizmo that allows you to choose one of several types of despill algorithms for keying. This node also allows the use of a background image to correct spill suppressed areas.

## Image
**RAMP**
A Shake style ramp

## Channel
**CHANNELSOLO**
Shuffles the chosen channel into RGBA

## Transform
**CROPBBOX**
Crops any bounding box outside of the input **width** and **height**.


## From init.py
Introduction
============
This script recursively adds path trees rooted in one or more directories to
the Nuke plugin path. If Nuke is running in GUI mode, it can also be used to
automatically build menu trees for any gizmo files it locates. (Note: see the
accompanying `menu.py` file for a predefined implementation of this.)

These root directories can be resolved in several ways. In order of precedence,
they are:

    1) Using the `CUSTOM_GIZMO_LOCATION` variable below, if it is set to an
        existing directory. Note that environment variables will be expanded.
    2) From the `NUKE_GIZMO_PATH` environment variable, if it is set.
    3) The location of the file in which the ``GizmoPathManager`` code resides.
    4) The Nuke plugin path.


Installation
============
To use the ``GizmoPathManager``, copy or move this file as-is to a directory on
your Nuke plugin path, or merge its contents with an existing `init.py` file.
The default directories included on the plugin path are:

Linux::

    /users/<LOGIN NAME>/.nuke
    /usr/local/Nuke6.2v6/plugins

Mac OS X::

    /Users/<LOGIN NAME>/.nuke
    /Applications/Nuke6.2v6/Nuke6.2v6.app/Contents/MacOS/plugins

Windows:
    In the .nuke directory, which can be found under the directory pointed to
    by the HOME environment variable. If this variable is not set (which is
    common), the .nuke directory will be under the folder specified by the
    USERPROFILE environment variable, which is generally in one of the
    following forms::

    <DRIVE LETTER>:\Documents and Settings\<LOGIN NAME>\    (Windows XP)
    <DRIVE LETTER>:\Users\<LOGIN NAME>\                     (Windows Vista/7)