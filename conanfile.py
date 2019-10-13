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
        generators = "cmake_paths"

        def _configure_cmake(self):
            cmake = CMake(self)
            conan_paths = os.path.join(self.build_folder, "conan_paths.cmake")
            cmake.definitions["CONAN_PACKAGE_VERSION"] = self.version.split('-')[0]
            cmake.definitions["CMAKE_FIND_PACKAGE_PREFER_CONFIG"] = "TRUE"
            cmake.definitions["CMAKE_PROJECT_INCLUDE"] = conan_paths
            cmake.generator = "Ninja"
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
