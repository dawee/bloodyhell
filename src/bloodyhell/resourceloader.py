import os
import re
import pygame

class ResourcesFolderMissing(Exception):
    """
    Raised if no resources folder has been set
    """

class ResourceLoader(object):

    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = object.__new__(self)
            self._instance._initialize()
        return self._instance

    def _initialize(self):
        self._resources_folder = None
        self._resources = {}
        self._screen = None

    def set_screen(self, screen):
        self._screen = screen

    def screen(self):
        return self._screen

    def set_resources_folder(self, folder):
        self._resources_folder = folder

    def browse_folder(self, package_name, dir_name, file_names):
        package_path = os.path.join(self._resources_folder, package_name)
        for file_name in file_names:
            file_path = os.path.abspath(os.path.join(dir_name, file_name))
            if os.path.isfile(file_path):
                resource_id = os.path.join(
                    os.path.relpath(dir_name, package_path),
                    os.path.splitext(file_name)[0]
                ).replace(os.path.sep, '.')
                self._resources[
                    package_name
                ][resource_id] = pygame.image.load(file_path)

    def load_package(self, package_name):
        if self._resources_folder is None:
            raise ResourcesFolderMissing(
                'Resources folder has not been set'
            )
        if not package_name in self._resources:
            self._resources[package_name] = {}
        package_path = os.path.join(self._resources_folder, package_name)
        os.path.walk(package_path, self.browse_folder, package_name)

    def get_resource(self, full_resource_id):
        package_name, resource_id = full_resource_id.split('.', 1)
        return self._resources[package_name][resource_id].copy()

    def get_animation_frames(self, full_resource_id_base):
        package_name, resource_id_base = full_resource_id_base.split('.', 1)
        pattern = re.compile('%s_([0-9]+)' % resource_id_base)
        frames = {}
        for resource_id in self._resources[package_name].keys():
            regex_object = pattern.match(resource_id)
            if regex_object:
                frames[int(regex_object.group(1))] = '%s.%s' % (package_name, resource_id)
        return frames

    def draw_image(self, full_resource_id, dest):
        package_name, resource_id = full_resource_id.split('.', 1)
        image = self._resources[package_name][resource_id]
        dest.set_width(image.get_width())
        dest.set_height(image.get_height())
        dest.blit(image, (0, 0))
