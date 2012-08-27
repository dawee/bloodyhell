import os
import sys
from zipfile import ZipFile


class Packager(object):

    def __init__(self, resources_path, output_path):
        try:
            os.makedirs(output_path)
        except:
            pass
        self._resources_path = os.path.abspath(resources_path)
        self._output_path = os.path.abspath(output_path)

    def save_all(self):
        for package_name in os.listdir(self._resources_path):
            if os.path.isdir(os.path.join(self._resources_path, package_name)):
                self.save(package_name)

    def _browse_sub_dir(self, options, dir_name, file_names):
        dat_file = options['dat_file']
        for file_name in file_names:
            file_path = os.path.join(dir_name, file_name)
            if os.path.isfile(file_path):
                dat_file.write(file_path, os.path.relpath(
                    file_path, options['package_path']
                ))

    def save(self, package_name):
        package_path = os.path.join(self._resources_path, package_name)
        output_dat_path = os.path.join(self._output_path, package_name + '.dat')
        dat_file = ZipFile(output_dat_path, 'w')
        os.path.walk(package_path, self._browse_sub_dir, {
            'dat_file': dat_file,
            'package_path': package_path
        })
        dat_file.close()


if __name__ == '__main__':
    packager = Packager(sys.argv[1], sys.argv[2])
    packager.save_all()
