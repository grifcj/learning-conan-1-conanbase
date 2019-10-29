from pathlib import Path
import json
import os
import shutil
import textwrap

from recordtype import recordtype

from conans import ConanFile, CMake, tools

class PythonRequires(ConanFile):
    name = "conanbase"
    version = "1.0.0-nightly"

def get_conanfile():
    class BaseConanFile(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False]}
        default_options = "shared=False"
        generators = ("cmake_paths", "cmake_find_package")

        def _make_proj_include(self):
            proj_inc = os.path.join(self.build_folder, 'project_include.cmake')
            with open(proj_inc, 'w') as f:
                f.write(textwrap.dedent(
                    """
                    include_guard(GLOBAL)
                    include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
                    list(PREPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
                    list(PREPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})
                    """)[1:])

            return proj_inc

        def _make_cmake(self):
            cmake = CMake(self)
            cmake.definitions["PACKAGE_VERSION"] = self.version.split('-')[0]
            cmake.definitions["CMAKE_PROJECT_INCLUDE"] = self._make_proj_include()
            return cmake

        def _configure_cmake(self):
            cmake = self._make_cmake()
            cmake.configure()
            return cmake

        def build(self):
            cmake = self._configure_cmake()
            cmake.build()
            cmake.test()

        def package(self):
            cmake = self._configure_cmake()
            cmake.install()
            for t in Path().glob('target-*-cpp-info.json'):
                self.copy(str(t), dst='package-info')

        def _cmake_targets(self):
            def to_list(cmake_list):
                return cmake_list.strip(';').split(';')

            for t in Path().glob('package-info/target-*-cpp-info.json'):
                with open(str(t), 'r') as f:
                    t = json.load(f, object_hook=lambda d: recordtype('target', d.keys())(*d.values()))
                    t.includedirs.build = to_list(t.includedirs.build)
                    t.includedirs.install = to_list(t.includedirs.install)
                    t.cflags = to_list(t.cflags)
                    t.cxxflags = to_list(t.cxxflags)
                    t.defines = to_list(t.defines)
                    t.requires = to_list(t.requires)
                    yield t

        def package_info(self):
            for t in self._cmake_targets():
                self.cpp_info.libs.extend([t.name])
                self.cpp_info.defines.extend(t.defines)
                self.cpp_info.cflags.extend(t.cflags)
                self.cpp_info.cxxflags.extend(t.cxxflags)
                if self.in_local_cache:
                    self.cpp_info.includedirs.extend(t.includedirs.install)
                else:
                    self.cpp_info.includedirs.extend(t.includedirs.build)

    return BaseConanFile
