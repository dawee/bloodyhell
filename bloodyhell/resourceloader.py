import os
import re
import sys
import pygame
import json
import tempfile
import uuid
import zipfile
from xml.dom.minidom import parse

from bloodyhell.layer.rect import Rect

class ResourcesFolderMissing(Exception):
    """
    Raised if no resources folder has been set
    """

class ResourceLoader(object):

    TMP_DIR = '.bhtmp'
    _instance = None

    TYPES = {
        '.png': 'add_image_resource',
        '.jpg': 'add_image_resource',
        '.jpeg': 'add_image_resource',
        '.mp3': 'add_sound_resource',
        '.json': 'add_json_resource',
        '.xml': 'add_xml_resource'
    }

    def __new__(self):
        if self._instance is None:
            self._instance = object.__new__(self)
            self._instance._initialize()
        return self._instance

    def _initialize(self):
        self._resources_folder = None
        self._resources = {}
        self._parent_package_path = ''
        self._screen = None
        self._sub_surfaces_ids = []

    def set_screen(self, screen):
        self._screen = screen

    def screen(self):
        return self._screen

    def set_resources_folder(self, folder):
        self._resources_folder = folder

    def browse_folder(self, package_name, dir_name, file_names):
        package_path = os.path.abspath(
            os.path.join(self._parent_package_path, package_name)
        )
        for file_name in file_names:
            file_path = os.path.abspath(os.path.join(dir_name, file_name))
            if os.path.isfile(file_path):
                if os.path.abspath(dir_name) == package_path:
                    resource_id = os.path.splitext(file_name)[0]
                else:
                    resource_id = os.path.join(
                        os.path.relpath(
                            os.path.abspath(dir_name),
                            package_path
                        ),
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
        self._resources[package][identity] = json.load(open(file_path))

    def add_xml_resource(self, package, identity, file_path):
        self._resources[package][identity] = parse(file_path)

    def load_folder_package(self, package_name):
        if self._resources_folder is None:
            raise ResourcesFolderMissing(
                'Resources folder has not been set'
            )
        if not package_name in self._resources:
            self._resources[package_name] = {}
        self._parent_package_path = self._resources_folder
        package_path = os.path.join(self._resources_folder, package_name)
        os.path.walk(package_path, self.browse_folder, package_name)

    def load_package(self, package_name):
        if not hasattr(sys, 'frozen'):
            self.load_folder_package(package_name)
        else:
            self.load_archive_package(package_name)

    def clean_lazy(self):
        """
        for sub_str in self._sub_surfaces_ids:
            package_name, resource_id = sub_str.split('.', 1)
            self._resources[package_name][resource_id] = None
            del self._resources[package_name][resource_id]
        self._sub_surfaces_ids = []
        """

    def get_resource(self, full_resource_id, rect, cropped_rect):
        package_name, resource_id = full_resource_id.split('.', 1)
        sub_surface_str = '%s_%s_%s' % (
            resource_id, rect.width, rect.height
        )
        self._sub_surfaces_ids.append('%s.%s' % (package_name, sub_surface_str))
        if sub_surface_str not in self._resources[package_name]:
            surface = self._resources[package_name][resource_id]
            self._resources[package_name][
                sub_surface_str
            ] = pygame.transform.scale(
                surface, (rect.width, rect.height)
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

    def get_width_from_ratio(self, resource_id, height):
        surface = self.get_raw_resource(resource_id)
        image_width = surface.get_width() * height / surface.get_height()
        return (image_width, height)

    def load_archive_package(self, package_name):
        if self._resources_folder is None:
            raise ResourcesFolderMissing(
                'Resources folder has not been set'
            )
        if not package_name in self._resources:
            self._resources[package_name] = {}
        tmp_path = os.path.abspath(os.path.join(
            tempfile.gettempdir(),
            self.TMP_DIR,
            str(uuid.uuid1())
        ))
        package_path = os.path.join(tmp_path, package_name)
        try:
            os.makedirs(package_path)
        except:
            pass
        dat_file = zipfile.ZipFile(os.path.join(
            self._resources_folder,
            package_name + '.dat'
        ))
        dat_file.extractall(package_path)
        self._parent_package_path = tmp_path
        os.path.walk(package_path, self.browse_folder, package_name)
