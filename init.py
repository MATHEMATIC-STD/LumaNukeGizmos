import os
import re

import nuke


# This can be used to set the root directory for the GizmoPathManager search
# without the need to define any environment variables. Note that if this is
# defined and points to an existing directory, other possible search locations
# will be ignored, unless the `__main__` entry point code is modified below.
CUSTOM_GIZMO_LOCATION = r''


class GizmoPathManager(object):
    '''
    Class used to automatically add directory trees to the Nuke plugin path,
    and to build menu items for any gizmos found in those trees.
    '''
    def __init__(self, searchPaths=None, exclude=r'^\.', ):
        '''
        'searchPaths': An iterable of paths to recursively search. If omitted,
        the search will first try to use the `NUKE_GIZMO_PATH` environment
        variable. If that is also undefined, it will resolve and use the
        directory in which this file resides. If that cannot be determined, the
        contents of the Nuke plugin path will be used.

        'exclude': A regular expression for folders and gizmo files to ignore.
        The default pattern ignores anything beginning with `.`.
        '''
        if isinstance(exclude, str):
            exclude = re.compile(exclude)
        self.exclude = exclude
        if searchPaths is None:
            searchPaths = os.environ.get('NUKE_GIZMO_PATH', '').split(os.pathsep)
            if not searchPaths:
                import inspect
                thisFile = inspect.getsourcefile(lambda: None)
                if thisFile:
                    searchPaths = [os.path.dirname(os.path.abspath(thisFile))]
                else:
                    searchPaths = list(nuke.pluginPath())
        self.searchPaths = searchPaths
        self.reset()

    @classmethod
    def canonical_path(cls, path):
        return os.path.normcase(os.path.normpath(os.path.realpath(os.path.abspath(path))))

    def reset(self):
        self._crawlData = {}

    def addGizmoPaths(self):
        '''
        Recursively search ``self.searchPaths`` for folders whose names do not
        match the exclusion pattern ``self.exclude``, and add them to the Nuke
        plugin path.
        '''
        self.reset()
        self._visited = set()
        for gizPath in self.searchPaths:
            self._recursiveAddGizmoPaths(gizPath, self._crawlData,
                                         foldersOnly=True)

    def _recursiveAddGizmoPaths(self, folder, crawlData, foldersOnly=False):
        # If we're in GUI mode, also store away data in _crawlDatato to be used
        # later by addGizmoMenuItems
        if not os.path.isdir(folder):
            return

        if nuke.GUI:
            if 'files' not in crawlData:
                crawlData['gizmos'] = []
            if 'dirs' not in crawlData:
                crawlData['dirs'] = {}

        # avoid an infinite loop due to symlinks...
        canonical_path = self.canonical_path(folder)
        if canonical_path in self._visited:
            return
        self._visited.add(canonical_path)

        for subItem in sorted(os.listdir(canonical_path)):
            if self.exclude and self.exclude.search(subItem):
                continue
            subPath = os.path.join(canonical_path, subItem)
            if os.path.isdir(subPath):
                nuke.pluginAppendPath(subPath)
                subData = {}
                if nuke.GUI:
                    crawlData['dirs'][subItem] = subData
                self._recursiveAddGizmoPaths(subPath, subData)
            elif nuke.GUI and (not foldersOnly) and os.path.isfile(subPath):
                name, ext = os.path.splitext(subItem)
                if ext == '.gizmo':
                    crawlData['gizmos'].append(name)

    def addGizmoMenuItems(self, rootMenu=None, defaultTopMenu=None):
        '''
        Recursively creates menu items for gizmos found on this instance's
        search paths. This only has an effect if Nuke is in GUI mode.

        'rootMenu': The root Nuke menu to which the menus and menu items should
        be added, either as a ``nuke.Menu`` object or a string. If omitted, the
        Nuke 'Nodes' menu will be used.

        'defaultTopMenu': If you do not wish to create new menu items at the
        top level of the target parent menu, directories for which top-level
        menus do not already exist will be added to this menu instead. This
        must be the name of an existing menu.
        '''
        if not nuke.GUI:
            return

        if not self._crawlData:
            self.addGizmoPaths()

        if rootMenu is None:
            rootMenu = nuke.menu('Nodes')
        elif isinstance(rootMenu, basestring):
            rootMenu = nuke.menu(rootMenu)
        self._recursiveAddGizmoMenuItems(rootMenu, self._crawlData,
                                         defaultSubMenu=defaultTopMenu,
                                         topLevel=True)

    def _recursiveAddGizmoMenuItems(self, toolbar, crawlData,
                                    defaultSubMenu=None, topLevel=False):
        for name in crawlData.get('gizmos', ()):
            niceName = name
            if niceName.find('_v')==len(name) - 4:
                niceName = name[:-4]
            toolbar.addCommand(niceName,"nuke.createNode('%s')" % name)

        for folder, data in crawlData.get('dirs', {}).items():
            import sys
            subMenu = toolbar.findItem(folder)
            if subMenu is None:
                if defaultSubMenu:
                    subMenu = toolbar.findItem(defaultSubMenu)
                else:
                    subMenu = toolbar.addMenu(folder, icon=folder + ".png")
            self._recursiveAddGizmoMenuItems(subMenu, data)


if __name__ == '__main__':
    CUSTOM_GIZMO_LOCATION = os.path.expandvars(CUSTOM_GIZMO_LOCATION.strip()).rstrip('/\\')
    if CUSTOM_GIZMO_LOCATION and os.path.isdir(CUSTOM_GIZMO_LOCATION):
        gizManager = GizmoPathManager(searchPaths=[CUSTOM_GIZMO_LOCATION])
    else:
        gizManager = GizmoPathManager()
    gizManager.addGizmoPaths()
    if not nuke.GUI:
        del gizManager
