import os
import re
import sys
import pygame
import json

from bloodyhell.layer.rect import Rect


class ResourcesFolderMissing(Exception):
    """
    Raised if no resources folder has been set
    """


class ResourceLoader(object):

    _instance = None

    TYPES = {
        '.png': 'add_image_resource',
        '.jpg': 'add_image_resource',
        '.jpeg': 'add_image_resource',
        '.wav': 'add_sound_resource',
        '.json': 'add_json_resource'
    }

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
                extension = os.path.splitext(file_name)[1]
                if extension in self.TYPES:
                    getattr(self, self.TYPES[extension])(
                        package_name, resource_id, file_path
                    )

    def add_image_resource(self, package, identity, file_path):
        self._resources[package][identity] = pygame.image.load(file_path)

    def add_sound_resource(self, package, identity, file_path):
        try:
            self._resources[package][identity] = pygame.mixer.Sound(file_path)
        except:
            sys.stderr.write('Failed to load sound !\n')

    def add_json_resource(self, package, identity, file_path):
        self._resources[package][identity] = json.load(file_path)

    def load_package(self, package_name):
        if self._resources_folder is None:
            raise ResourcesFolderMissing(
                'Resources folder has not been set'
            )
        if not package_name in self._resources:
            self._resources[package_name] = {}
        package_path = os.path.join(self._resources_folder, package_name)
        os.path.walk(package_path, self.browse_folder, package_name)

    def get_resource(self, full_resource_id, rect, cropped_rect):
        package_name, resource_id = full_resource_id.split('.', 1)
        sub_surface_str = '%s_%s_%s_%s_%s_%s_%s_%s_%s' % (
            resource_id,
            cropped_rect.x, cropped_rect.y,
            cropped_rect.width, cropped_rect.height,
            rect.x, rect.y,
            rect.width, rect.height,
        )
        if sub_surface_str not in self._resources[package_name]:
            surface = self._resources[package_name][resource_id]
            cropped_surface = surface.subsurface(Rect(
                cropped_rect.x * surface.get_width() / rect.width,
                cropped_rect.y * surface.get_height() / rect.height,
                cropped_rect.width * surface.get_width() / rect.width,
                cropped_rect.height * surface.get_height() / rect.height
            ))
            self._resources[package_name][
                sub_surface_str
            ] = pygame.transform.scale(
                cropped_surface,
                (cropped_rect.width, cropped_rect.height)
            )
        return self._resources[package_name][sub_surface_str]

    def get_raw_resource(self, full_resource_id):
        package_name, resource_id = full_resource_id.split('.', 1)
        return self._resources[package_name][resource_id]

    def play_sound(self, full_resource_id):
        package_name, resource_id = full_resource_id.split('.', 1)
        sound = self._resources[package_name][resource_id]
        sound.play()

    def get_animation_frames(self, full_resource_id_base):
        package_name, resource_id_base = full_resource_id_base.split('.', 1)
        pattern = re.compile('%s_([0-9]+)' % resource_id_base)
        frames = {}
        for resource_id in self._resources[package_name].keys():
            regex_object = pattern.match(resource_id)
            if regex_object:
                frames[
                    int(regex_object.group(1))
                ] = '%s.%s' % (package_name, resource_id)
        return frames
