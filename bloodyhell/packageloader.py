import os
import zipfile
import uuid
import tempfile

from bloodyhell.resourceloader import ResourceLoader, ResourcesFolderMissing


class PackageLoader(ResourceLoader):

    TMP_DIR = '.bhtmp'

    def load_package(self, package_name):
        if self._resources_folder is None:
            raise ResourcesFolderMissing(
                'Resources folder has not been set'
            )
        if not package_name in self._resources:
            self._resources[package_name] = {}
        tmp_path = os.path.join(
            tempfile.gettempdir(),
            self.TMP_DIR,
            uuid.uuid1()
        )
        try:
            os.makedirs(tmp_path)
        except:
            pass
        dat_file = zipfile.ZipFile(os.path.join(
            self._resources_folder,
            package_name + '.dat'
        ))
        dat_file.extractall(tmp_path)
        os.path.walk(tmp_path, self.browse_folder, package_name)
