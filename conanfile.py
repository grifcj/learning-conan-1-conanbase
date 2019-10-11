import os
import shutil
from conans import ConanFile, CMake, tools

def get_version():
    git = tools.Git()
    try:
        # Use long format so that semver interprets every version as a
        # pre-release and hence they can be sorted in monotonic order as far as
        # conan's version ranges are concerned.
        return git.run("describe --tags --dirty --always --long").replace('/', '-')
    except:
        return None

class PythonRequires(ConanFile):
    name = "conanbase"
    version = get_version()

def get_conanfile():
    class BaseConanFile(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False]}
        default_options = "shared=False"

        def _configure_cmake(self):
            cmake = CMake(self)
            cmake.configure()
            return cmake

        def build(self):
            cmake = self._configure_cmake()
            cmake.build()
            cmake.test()

        def package(self):
            cmake = self._configure_cmake()
            cmake.install()

    return BaseConanFile
