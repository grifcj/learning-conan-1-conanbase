import os
import shutil
from conans import ConanFile, CMake, tools

class PythonRequires(ConanFile):
    name = "conanbase"
    version = "1.0.0-nightly"

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
